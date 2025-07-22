import streamlit as st
import pandas as pd
from io import BytesIO
from utils.session_state import SessionStateManager
from file_handler import FileHandler


def render_results():
    """
    Display the final results dataframe and provide an Excel download.
    """
    st.header("📊 Results")
    SessionStateManager.initialize()

    result_df: pd.DataFrame = st.session_state.get("results", pd.DataFrame())
    if result_df.empty:
        st.error("No results available. Please complete the analysis step first.")
        return

    # Show results table
    st.dataframe(result_df, use_container_width=True)

    # Generate Excel report bytes
    try:
        excel_bytes: bytes = FileHandler.create_excel_bytes(
            results=result_df
        )
    except Exception as e:
        st.error(f"Failed to generate Excel report: {e}")
        return

    # Download button
    st.download_button(
        label="📥 Download Excel Report",
        data=excel_bytes,
        file_name="PTA_Analysis_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
