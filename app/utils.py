import json

import pandas as pd
import streamlit as st
from sklearn.metrics import precision_recall_fscore_support

DIMENSIONS_DESCRIPTIONS = {
    "LRGEN": "supports left/right ideology overall",
    "LRECON": "supports left/right economic ideology, role of government in economy",
    "GALTAN": "libertarian vs traditional/authoritarian view",
    "SPENDVTAX": "favors improving public services vs reducing taxes",
    "DEREGULATION": "opposes/supports deregulation of markets",
    "REDISTRIBUTION": "favors/opposes redistribution of wealth",
    "ECON_INTERVEN": "favors/opposes state intervention in economy",
    "CIVLIB_LAWORDER": "promotes civil liberties vs tough measures against crime",
    "SOCIALLIFESTYLE": "supports/opposes liberal policies (e.g. homosexual rights)",
    "RELIGIOUS_PRINCIPLES": "opposes/supports religious principles in politics",
    "IMMIGRATE_POLICY": "favors liberal vs restrictive immigration policy",
    "MULTICULTURALISM": "favors multiculturalism vs assimilation",
    "URBAN_RURAL": "supports urban vs rural interests",
    "ENVIRONMENT": "supports environmental protection vs economic growth",
    "COSMO": "advocates cosmopolitanism vs nationalism",
    "PROTECTIONISM": "favors trade liberalization vs protection of domestic producers",
    "REGIONS": "favors/opposes political decentralization",
    "INTERNATIONAL_SECURITY": "favors/opposes troop deployment",
    "ETHNIC_MINORITIES": "supports/opposes more rights for ethnic minorities",
    "EU_INTEGRATION": "opposes/supports EU integration"
}


@st.cache_data(show_spinner=False)
def load_jsonl_results(file_path):
    """Load results from JSONL file."""
    results = []
    with open(file_path, "r") as f:
        for line in f:
            results.append(json.loads(line))
    return pd.DataFrame(results)


def calculate_metrics(topics_data, labeled_data):
    """Calculate precision, recall, and F1 score using scikit-learn."""
    if not labeled_data:
        return {"precision": 0, "recall": 0, "f1": 0}
    
    y_true = []
    y_pred = []
    
    for topic_id, user_dimensions in labeled_data.items():
        # Find the topic in the dataset
        topic_entry = next((topic for topic in topics_data if topic["id"] == topic_id), None)
        if not topic_entry or "hypotheses" not in topic_entry:
            continue
        
        true_dimensions = set()
        for hypothesis in topic_entry["hypotheses"]:
            true_dimensions.add(hypothesis["dimension"])

        all_dimensions = list(DIMENSIONS_DESCRIPTIONS.keys())
        
        true_vector = [1 if dim in true_dimensions else 0 for dim in all_dimensions]
        pred_vector = [1 if dim in user_dimensions else 0 for dim in all_dimensions]
        
        y_true.append(true_vector)
        y_pred.append(pred_vector)
    
    if not y_true or not y_pred:
        return {"precision": 0, "recall": 0, "f1": 0}

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='micro', zero_division=0
    )
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1
    }