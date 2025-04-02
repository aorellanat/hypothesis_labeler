import streamlit as st
import json
import pandas as pd


def ideological_dimensions_box():
    with  st.expander("Ideological dimensions (click to expand)", expanded=False):
        st.write(f'''
        1. **LRGEN**: (left: "supports left ideology overall", right: "supports right ideology overall") 
        2. **LRECON**: (left: "supports left economic ideology, supports active role of government in economy", right: "supports right economic ideology, supports reduced role of government in economy")
        3. **GALTAN**: (left: "libertarian/postmaterialist view, supports expanded personal freedoms", right : "traditional/authoritarian view, supports government as moral authority")
        4. **SPENDVTAX**: (left: "favors improving public services", right: "favors reducing taxes")
        5. **DEREGULATION**: (left: "opposes deregulation of markets ", right: "supports deregulation of markets")
        6. **REDISTRIBUTION**: (left: "favors redistribution of wealth", right: "opposes redistribution of wealth")
        7. **ECON_INTERVEN**: (left: "in favor of state intervention in economy", right: "opposes state intervention in economy")
        8. **CIVLIB_LAWORDER**: (left: "promotes civil liberties", right: "supports tough measures to fight crime")
        9. **SOCIALLIFESTYLE:** (left: "supports liberal policies regarding social lifestyle (e.g. homosexual rights, gender equality)", right: "opposes liberal policies regarding social lifestyle")
        10. **RELIGIOUS_PRINCIPLES**: (left: "opposes religious principles in politics", right: "supports religious principles in politics")
        11. **IMMIGRATE_POLICY**: (left: "favors a liberal policy on immigration", right: "favors a restrictive policy on immigration")
        12. **MULTICULTURALISM**: (left: "favors multiculturalism", right: "favors assimilation")
        13. **URBAN_RURAL**: (left: "supports urban interests", right: "supports rural interests")
        14. **ENVIRONMENT**: (left: "supports environmental protection even at the cost of economic growth", right: "supports economic growth even at the cost of environmental protection")
        15. **COSMO**: (left: "advocates cosmopolitanism", right: "advocates nationalism")
        16. **PROTECTIONISM**: (left: "favors trade liberalization", right: "favors protection of domestic producers")
        17. **REGIONS**: (left: "favors political decentralization", right: "opposes political decentralization")
        18. **INTERNATIONAL_SECURITY**: (left: "favors troop deployment", right: "opposes troop deployment")
        19. **ETHNIC_MINORITIES**: (left: "supports more rights for ethnic minorities", right: "opposes more rights for ethnic minorities")
        20. **EU_INTEGRATION**: (left: "opposes EU integration", right: "supports EU integration")
        ''')


def criteria_box(hypothesis_id: str, dimension: str, current_labels: dict = None):
    with st.container(border=True):
        st.write("""
        **Evaluation criteria:** Please assess whether the hypothesis meets the following requirements:
        """)

        if current_labels is None:
            current_labels = {
                'clarity': None,
                'relevance': None,
            }

        # Initialize session state for this hypothesis if not exists
        if f"labels_{hypothesis_id}_{dimension}" not in st.session_state:
            st.session_state[f"labels_{hypothesis_id}_{dimension}"] = current_labels

        criteria = {
            'clarity': "Is the hypothesis clearly and coherently stated?",
            'relevance': "Does the hypothesis explicitly address the specified topic and clearly connect it to a relevant ideological dimension?",
        }

        for criterion, question in criteria.items():
            st.write(f"**{question}**")
            col1, col2 = st.columns([3, 1])
            with col1:
                response = st.radio(
                    f"Response for {criterion}",
                    options=["Select", "Yes", "No"],
                    key=f"{hypothesis_id}_{dimension}_{criterion}",
                    horizontal=True,
                    label_visibility="collapsed",
                    index=0
                )

                if response != "Select":
                    st.session_state[f"labels_{hypothesis_id}_{dimension}"][criterion] = response.lower()

        # Update labeled_data in session state only if all criteria have been selected
        all_selected = all(label is not None for label in st.session_state[f"labels_{hypothesis_id}_{dimension}"].values())
        if all_selected:
            topic_id, hypothesis_idx = hypothesis_id.split('_')
            st.session_state.labeled_data[(topic_id, int(hypothesis_idx))] = st.session_state[f"labels_{hypothesis_id}_{dimension}"]

        st.markdown("---")
        st.write("**Current labels:**")
        col1, col2 = st.columns(2)
        for i, (criterion, label) in enumerate(st.session_state[f"labels_{hypothesis_id}_{dimension}"].items()):
            with col1 if i == 0 else col2:
                if label:
                    icon = ":material/check:" if label == "yes" else ":material/close:"
                    st.info(f"{criterion.replace('_', ' ').title()}: {label.upper()}", icon=icon)
                else:
                    st.warning(f"{criterion.replace('_', ' ').title()}: Not selected yet")


def save_labeled_hypotheses(hypotheses: pd.DataFrame):
    return hypotheses.to_json(orient='records', lines=True)


def display_hypothesis(hypothesis):
    st.markdown(f"""
    <div style='
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #2E9BF5;
        position: relative;
    '>
        <div style='
            font-size: 24px;
            color: #2E9BF5;
            position: absolute;
            top: 10px;
            left: 10px;
        '>❝</div>
        <div style='
            padding-left: 25px;
            padding-top: 10px;
            font-style: italic;
            color: #2E9BF5;
        '>
            {hypothesis['hypothesis']}
        </div>
        <div style='
            font-size: 24px;
            color: #2E9BF5;
            position: absolute;
            bottom: 0;
            right: 20px;
        '>❞</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #229954;
    '>
        <div style='
            color: #1a1a1a;
            font-size: 1em;
            line-height: 1.6;
        '>
            <span style='font-weight: bold;'>Dimension:</span>
            {hypothesis['dimension']}
        </div>
    </div>
    """, unsafe_allow_html=True)


def main(
    hypotheses_path: str = "app/hypotheses_31_03_2025_17_48_32.jsonl",
):
    if 'current_topic_idx' not in st.session_state:
        st.session_state.current_topic_idx = 0
    if 'current_hypothesis_idx' not in st.session_state:
        st.session_state.current_hypothesis_idx = 0
    if 'labeled_data' not in st.session_state:
        st.session_state.labeled_data = {}

    with open(hypotheses_path, "r") as f:
        hypotheses = pd.DataFrame([json.loads(line) for line in f])

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Hypothesis labeler")
    with col2:
        st.markdown("""
            <style>
            .save-button button {
                height: 35px;
                font-size: 0.9em;
                margin-top: 15px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        labeled_data = []
        for (topic_id, hypothesis_idx), labels in st.session_state.labeled_data.items():
            topic_row = hypotheses[hypotheses['id'] == topic_id].iloc[0]
            hypothesis = topic_row['hypotheses'][hypothesis_idx]
            labeled_data.append({
                'topic_id': topic_id,
                'topic': topic_row['topic'],
                'top_term': topic_row['top_term'],
                'hypothesis': hypothesis['hypothesis'],
                'dimension': hypothesis['dimension'],
                'labels': labels
            })
        
        if labeled_data:
            json_data = save_labeled_hypotheses(pd.DataFrame(labeled_data))
            st.download_button(
                label="💾 Save progress",
                data=json_data,
                file_name="labeled_hypotheses.jsonl",
                mime="application/json",
                use_container_width=True,
                key="save_button"
            )
        else:
            st.download_button(
                label="💾 Save progress",
                data="",
                file_name="labeled_hypotheses.jsonl",
                mime="application/json",
                use_container_width=True,
                key="save_button",
                disabled=True
            )

    total_topics = len(hypotheses)
    remaining_topics = total_topics - st.session_state.current_topic_idx
    total_hypotheses = sum(len(row['hypotheses']) for _, row in hypotheses.iterrows())
    
    labeled_hypotheses = len(st.session_state.labeled_data)

    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-size: 1.2em;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.9em;
        }
        </style>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Topics remaining", f"{remaining_topics}/{total_topics}")
    with col2:
        st.metric("Hypotheses labeled", f"{labeled_hypotheses}/{total_hypotheses}")

    ideological_dimensions_box()

    if st.session_state.current_topic_idx < len(hypotheses):
        current_topic = hypotheses.iloc[st.session_state.current_topic_idx]
        current_hypotheses = current_topic['hypotheses']
        
        st.markdown("""
            <style>
            .topic-info {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 5px solid #9B59B6;
            }
            .topic-info h6 {
                color: #9B59B6;
                font-weight: bold;
            }
            .topic-info p {
                margin: 0;
                color: #1a1a1a;
            }
            .topic-stats {
                display: flex;
                gap: 40px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="topic-info">
                <h6>Topic: {current_topic['topic']}</h6>
                <div class="topic-stats">
                    <p><strong>Top term (more general concept for this topic):</strong> {current_topic['top_term']}</p>
                    <p><strong>Number of hypotheses for this topic:</strong> {len(current_hypotheses)}</p>
                    <p><strong>Progress:</strong> Hypothesis {st.session_state.current_hypothesis_idx + 1} of {len(current_hypotheses)}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.current_hypothesis_idx < len(current_hypotheses):
            current_hypothesis = current_hypotheses[st.session_state.current_hypothesis_idx]
            
            display_hypothesis(current_hypothesis)
            
            hypothesis_key = f"{current_topic['id']}_{st.session_state.current_hypothesis_idx}"
            current_labels = st.session_state.labeled_data.get(hypothesis_key)
            
            criteria_box(hypothesis_key, current_hypothesis['dimension'], current_labels)

            st.markdown("""
                <style>
                div.navigation-button button {
                    width: 100%;
                    height: 50px;
                    margin: 10px 0;
                }
                </style>
            """, unsafe_allow_html=True)

            col1, _, col3 = st.columns([0.5, 2, 0.5])
            with col1:
                if st.button("⬅️ Previous", 
                         disabled=st.session_state.current_topic_idx == 0 and st.session_state.current_hypothesis_idx == 0,
                         use_container_width=True):
                    if st.session_state.current_hypothesis_idx > 0:
                        st.session_state.current_hypothesis_idx -= 1
                    elif st.session_state.current_topic_idx > 0:
                        st.session_state.current_topic_idx -= 1
                        st.session_state.current_hypothesis_idx = len(hypotheses.iloc[st.session_state.current_topic_idx]['hypotheses']) - 1
                    st.rerun()

            with col3:
                if st.button("Next ➡️", use_container_width=True):
                    if st.session_state.current_hypothesis_idx < len(current_hypotheses) - 1:
                        st.session_state.current_hypothesis_idx += 1
                    else:
                        st.session_state.current_topic_idx += 1
                        st.session_state.current_hypothesis_idx = 0
                    st.rerun()

    else:
        st.success("🎉 All topics have been reviewed")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Stance detection",
        page_icon="🎯",
        layout="wide"
    )
    
    main()
