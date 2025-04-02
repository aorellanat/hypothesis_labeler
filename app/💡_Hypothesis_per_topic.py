import streamlit as st
import sys
import pandas as pd
import json

from pathlib import Path

project_root = Path().absolute()
sys.path.append(str(project_root))


@st.cache_data(show_spinner=False)
def load_hypotheses(file_path):
    """Load hypotheses from JSONL file."""
    hypotheses = []
    with open(file_path, 'r') as f:
        for line in f:
            hypotheses.append(json.loads(line))
    return pd.DataFrame(hypotheses)


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


def main(
    hypotheses_file: str = 'app/hypotheses_31_03_2025_17_48_32.jsonl'
):
    st.set_page_config(
        page_title="Topic Hypotheses",
        page_icon="💡",
        layout="wide"
    )

    st.title("💡 Topic hypotheses")

    if not Path(hypotheses_file).exists():
        st.error("No hypotheses file found. Please ensure the file exists")
        return

    df_topic_hypotheses = load_hypotheses(hypotheses_file)

    # Add category filter
    col1, col2, _ = st.columns([1, 1, 1])
    with col1:
        # Map original categories to display categories
        category_mapping = {
            "easy": "Non-technical topics",
            "technical": "Technical topics",
            "intermediate": "Technical topics"
        }
        
        # Create a new column with mapped categories
        df_topic_hypotheses['display_category'] = df_topic_hypotheses['category'].map(category_mapping)
        display_categories = sorted(df_topic_hypotheses['display_category'].unique())
        
        selected_display_category = st.selectbox(
            "Filter by category",
            ["All"] + display_categories
        )

    ideological_dimensions_box()

    with col2:
        # Filter topics based on selected display category
        filtered_df = df_topic_hypotheses
        if selected_display_category != "All":
            filtered_df = df_topic_hypotheses[
                df_topic_hypotheses['display_category'] == selected_display_category
            ]
        
        all_topics = sorted(filtered_df['topic'].unique())
        selected_topic = st.selectbox(
            "Select a topic to explore",
            ["All"] + all_topics,
            index=1
        )

    if selected_topic != "All":
        df_topic_data = filtered_df[filtered_df['topic'] == selected_topic]

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"###### Topic: {selected_topic} (ID: {df_topic_data['id'].iloc[0]})")
        with col2:
            # Only show top term if it's not null
            top_term = df_topic_data['top_term'].iloc[0]
            if pd.notna(top_term):
                st.markdown(f"###### General concept: {top_term}")

        df_hypotheses_to_show = df_topic_data
    else:
        df_hypotheses_to_show = filtered_df

    for _, row in df_hypotheses_to_show.iterrows():
        if selected_topic == "All":
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"###### {row['topic']} (ID: {row['id']})")
            with col2:
                # Only show top term if it's not null
                if pd.notna(row['top_term']):
                    st.markdown(f"###### General concept: {row['top_term']}")

        with st.container():
            for i, hypothesis in enumerate(row['hypotheses']):
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
                        font-size: 1.1em;
                    '>
                        {i+1}. {hypothesis['hypothesis']}
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
                        <br>
                        <span style='font-weight: bold;'>Explanation:</span>
                        {hypothesis['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("---")

if __name__ == "__main__":
    main() 