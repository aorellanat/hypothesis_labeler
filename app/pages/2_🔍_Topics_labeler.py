import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

project_root = Path().absolute()
sys.path.append(str(project_root))

from app.utils import DIMENSIONS_DESCRIPTIONS, calculate_metrics, load_jsonl_results


def initialize_session_state(sampled_topics_path: str, hypotheses_path: str):
    if "topics_data" not in st.session_state:
        df_sampled_topics = load_jsonl_results(sampled_topics_path)
        unique_topic_ids = df_sampled_topics['id'].unique()

        df_topics_data = load_jsonl_results(hypotheses_path)
        st.session_state.topics_data = df_topics_data[df_topics_data['id'].isin(unique_topic_ids)]

    if "current_topic_idx" not in st.session_state:
        st.session_state.current_topic_idx = 0
    
    if "labeled_topics" not in st.session_state:
        st.session_state.labeled_topics = {}
    
    if "labeled_topic_ids" not in st.session_state:
        st.session_state.labeled_topic_ids = set()


def display_ideological_dimensions(current_selections=None):
    """Display checkboxes for all ideological dimensions."""
    selected_dimensions = []
    
    with st.container(border=True):
        st.write("What ideological dimensions are relevant to this topic?")

        cols = st.columns(2)
        for i, dimension in enumerate(DIMENSIONS_DESCRIPTIONS.keys()):
            col_idx = i % 2
            with cols[col_idx]:
                label = f"**{dimension}**: {DIMENSIONS_DESCRIPTIONS[dimension]}"
                # Use a unique key for each topic's dimension
                key = f"dim_{st.session_state.current_topic_idx}_{dimension}"

                # Set initial value based on current selections
                initial_value = dimension in current_selections if current_selections else False
                selected = st.checkbox(
                    label,
                    key=key,
                    value=initial_value
                )
                
                if selected:
                    selected_dimensions.append(dimension)
        
        return selected_dimensions

def main(
    sampled_topics_path: str = "app/sampled_hypotheses_42.jsonl",
    hypotheses_path: str = "app/hypotheses_09_04_2025_10_38_54.jsonl",
    output_path: str = 'topics_ideological_dimensions',
    output_path_metrics: str = 'topics_ideological_dimensions_metrics',
):
    initialize_session_state(sampled_topics_path, hypotheses_path)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🔍 Topics labeler")
    with col2:
        if st.session_state.labeled_topics and st.session_state.current_topic_idx < len(st.session_state.topics_data):
            st.download_button(
                label="💾 Save labeled topics",
                data=json.dumps(st.session_state.labeled_topics),
                file_name=f"{output_path}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Display progress metrics
    total_topics = len(st.session_state.topics_data)
    topics_labeled = len(st.session_state.labeled_topic_ids)
    progress = topics_labeled / total_topics if total_topics > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Topics", total_topics)
    with col2:
        st.metric("Topics Labeled", topics_labeled)
    with col3:
        st.metric("Progress", f"{progress:.1%}")
    
    st.progress(progress)
    
    # Display current topic
    if st.session_state.current_topic_idx < len(st.session_state.topics_data):
        current_topic = st.session_state.topics_data.iloc[st.session_state.current_topic_idx]
        topic_id = current_topic["id"]
        
        top_term_html = ""
        if current_topic.get("top_term") and pd.notna(current_topic["top_term"]):
            top_term_html = (
                "<br><span style='font-weight: bold;'>"
                f"Top term:</span> {current_topic['top_term']}"
            )

        st.markdown(
            f"""
            <div style='
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 5px solid #2E9BF5;
            '>
                <div style='
                    color: #1a1a1a;
                    font-size: 1em;
                    line-height: 1.6;
                '>
                    <span style='font-weight: bold; color: #2E9BF5;'>Topic: {current_topic['topic']} (ID: {topic_id})</span> 
                    {top_term_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        current_selections = st.session_state.labeled_topics.get(topic_id, [])
        selected_dimensions = display_ideological_dimensions(current_selections)
        
        if selected_dimensions != current_selections:
            st.session_state.labeled_topics[topic_id] = selected_dimensions
        
        st.markdown("""
            <style>
            .navigation-buttons {
                margin-top: 1rem;
            }
            </style>
            <div class="navigation-buttons">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous", 
                    disabled=st.session_state.current_topic_idx == 0,
                    use_container_width=True):
                st.session_state.current_topic_idx -= 1
                st.rerun()
        
        with col3:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.labeled_topic_ids.add(topic_id)
                if st.session_state.current_topic_idx < total_topics - 1:
                    st.session_state.current_topic_idx += 1
                else:
                    st.session_state.current_topic_idx += 1
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        topics_list = st.session_state.topics_data.to_dict('records')
        metrics = calculate_metrics(topics_list, st.session_state.labeled_topics)
        
        st.success("🎉 All topics have been reviewed!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Please save the labeled data (contains topics and the selected dimensions) and metrics.")
        with col2:
            st.download_button(
                label="💾 Save labeled topics",
                data=json.dumps(st.session_state.labeled_topics),
                file_name=f"{output_path}.json",
                mime="application/json",
                use_container_width=True
            )
        with col3:
            st.download_button(
                label="📊 Save metrics",
                data=json.dumps(metrics),
                file_name=f"{output_path_metrics}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.write("### Evaluation metrics")
        metrics_cols = st.columns(3)
        with metrics_cols[0]:
            st.metric("Precision", f"{metrics['precision']:.2f}")
        with metrics_cols[1]:
            st.metric("Recall", f"{metrics['recall']:.2f}")
        with metrics_cols[2]:
            st.metric("F1 Score", f"{metrics['f1']:.2f}")


if __name__ == "__main__":
    main() 