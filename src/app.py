import streamlit as st

from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT, INITIAL_SIDEBAR_STATE
from ui.sidebar import render_sidebar
from ui.uploads import render_upload_section
from ui.analysis import render_analysis
from ui.results import render_results
from utils.session_state import SessionStateManager


def main():
    """
    Configure the Streamlit page and orchestrate the app workflow.
    """
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    )

    # Initialize session state
    SessionStateManager.initialize()

    # Render sidebar navigation
    render_sidebar()

    # Route to the appropriate view
    step = st.session_state.current_step
    if step == "upload":
        # Upload view handles rerun to move to analysis
        render_upload_section()
    elif step == "analysis":
        # Perform analysis and store results
        if st.session_state.results is None:
            old_df = st.session_state.input_excel_old
            new_df = st.session_state.input_excel_new
            # Lazy import to avoid circular
            from data_processing import generate_results_df

            st.session_state.results = generate_results_df(
                old_df=old_df,
                new_df=new_df,
                pta_type=st.session_state.get("pta_type", "VP"),
            )
            st.session_state.analysis_completed = True
        render_analysis()
    elif step == "results":
        render_results()
    else:
        st.error(f"Unknown step: {step}")


if __name__ == "__main__":
    main()
