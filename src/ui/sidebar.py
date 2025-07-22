import streamlit as st
from typing import List, Dict
from utils.session_state import SessionStateManager


def render_sidebar():
    """
    Render the application sidebar with workflow navigation and project info.
    """
    SessionStateManager.initialize()

    st.sidebar.title("🚀 Project Workflow")
    steps: List[Dict[str, str]] = [
        {"key": "upload", "title": "📁 Upload Files", "description": "Upload PTA Excel files"},
        {"key": "analysis", "title": "🔍 Analysis & Visualization 📈", "description": "Perform analysis and visualization"},
        {"key": "results", "title": "📊 Results", "description": "View result dataframe and download Excel report"},
    ]

    current_step = st.session_state.get("current_step", "upload")
    for step in steps:
        is_current = current_step == step["key"]
        is_completed = is_step_completed(step["key"])

        icon = "🔵" if is_current else ("✅" if is_completed else "⚪")
        btn_type = "primary" if is_current else "secondary"

        col1, col2 = st.sidebar.columns([1, 4])
        col1.markdown(f"<div style='font-size:1.2rem'>{icon}</div>", unsafe_allow_html=True)
        if col2.button(step["title"], key=f"step_{step['key']}", type=btn_type, use_container_width=True):
            st.session_state.current_step = step["key"]
            st.experimental_rerun()

    st.sidebar.divider()
    st.sidebar.title("ℹ️ About Project")
    with st.sidebar.expander("Project Details", expanded=False):
        st.markdown(
            """
            This application compares two PTA Excel files to detect vehicle spring changes.

            **Key Features:**
            - 📊 Statistical Analysis
            - 🔍 Change Detection  
            - 📈 Data Visualization
            - 📋 Results Dashboard
            - 📥 Excel Export

            **Supported Files:**
            - Old PTA Excel file
            - New PTA Excel file
            """
        )


def is_step_completed(step_key: str) -> bool:
    """
    Check if a workflow step is completed based on session state.
    """
    ss = st.session_state
    if step_key == "upload":
        return ss.get("input_excel_old") is not None and ss.get("input_excel_new") is not None
    if step_key in ["analysis", "results"]:
        return ss.get("analysis_completed", False)
    return False
