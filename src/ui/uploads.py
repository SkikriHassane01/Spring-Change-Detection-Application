import streamlit as st
from typing import Optional
from utils.session_state import SessionStateManager
from file_handler import FileHandler
import pandas as pd


def render_upload_section() -> Optional[pd.DataFrame]:
    """
    Render the upload UI for old and new PTA Excel files.

    Returns:
        Tuple of (old_df, new_df) if both uploads are valid; otherwise None.
    """
    SessionStateManager.initialize()
    st.header("📁 Upload PTA Files")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Old PTA File")
        old_file = st.file_uploader(
            "Upload old PTA Excel", type=st.secrets.get("allowed_extensions", ["xlsx", "xls"])
        )
        if old_file is not None:
            valid, msg, df_old = FileHandler.validate_excel_file(old_file, "old")
            st.write(msg)
            if valid:
                SessionStateManager.clear_all()
                st.session_state.input_excel_old = df_old

    with col2:
        st.subheader("New PTA File")
        new_file = st.file_uploader(
            "Upload new PTA Excel", type=st.secrets.get("allowed_extensions", ["xlsx", "xls"])
        )
        if new_file is not None:
            valid, msg, df_new = FileHandler.validate_excel_file(new_file, "new")
            st.write(msg)
            if valid:
                st.session_state.input_excel_new = df_new

    if st.session_state.input_excel_old is not None and st.session_state.input_excel_new is not None:
        st.success("Both files uploaded successfully!")
        st.session_state.current_step = "analysis"
        st.experimental_rerun()

    return None
