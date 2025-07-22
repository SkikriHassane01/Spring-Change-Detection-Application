
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.session_state import SessionStateManager
from data_processing import generate_results_df

def render_overview(result_df: pd.DataFrame) -> None:
    """
    Display high-level metrics for the comparison.
    """
    st.header("📊 Analysis Overview")

    if result_df.empty:
        st.info("No data available for analysis.")
        return
    
    total_cars = len(result_df)
    total_new = (result_df["Change Type"] == "New").sum()
    total_spring = (result_df["Change Type"] == "Spring Changed").sum()
    total_unchanged = (result_df["Change Type"] == "Unchanged").sum()
    fleet_mass_change = result_df["Mass Difference"].sum()
    fleet_mass_total = result_df["New Mass"].sum() + result_df["Old Mass"].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚗 Total Cars in New File", total_cars)
    with col2:
        st.metric("🟥 New Cars", total_new,
                  help="Cars that did not exist in the old PTA file")
    with col3:
        st.metric("🔁 Spring Changed Cars", total_spring,
                  f"{(total_spring / total_cars) * 100:.1f} %")

    col4, col5 = st.columns(2)
    with col4:
        st.metric("✅ Unchanged Cars", total_unchanged)
    with col5:
        st.metric("⚖️ Fleet Mass Change", f"{fleet_mass_change:.2f} kg",
                  delta=f"{(fleet_mass_change / fleet_mass_total) * 100:.2f} %")


def render_mass_distribution(result_df: pd.DataFrame) -> None:
    """
    Show a pie chart of mass change status distribution.
    """
    st.subheader("📦 Mass Change Distribution")
    if result_df.empty:
        st.info("No data available for mass analysis.")
        return

    counts = result_df["Mass Status"].value_counts()
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title="Mass Status Overview"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_change_type_distribution(result_df: pd.DataFrame) -> None:
    """
    Display a bar chart of change type counts.
    """
    st.subheader("🔄 Change Type Distribution")
    if result_df.empty:
        st.info("No data available for change type analysis.")
        return

    counts = result_df["Change Type"].value_counts()
    fig = px.bar(
        x=counts.index,
        y=counts.values,
        title="Car Change Classification",
        labels={"x": "Change Type", "y": "Count"}
    )
    st.plotly_chart(fig, use_container_width=True)


def render_summary_statistics(result_df: pd.DataFrame) -> None:
    """
    Show summary statistics for mass differences, excluding new entries.
    """
    st.subheader("📈 Statistical Summary of Mass Differences")
    if result_df.empty:
        st.info("No data available for statistics.")
        return

    matched = result_df[result_df["Change Type"] != "New"]
    stats = {
        "Metric": [
            "Count", "Mean Change", "Std Deviation",
            "Min Change", "Max Change",
            "25th Percentile", "Median", "75th Percentile"
        ],
        "Value (kg)": [
            len(matched),
            matched["Mass Difference"].mean(),
            matched["Mass Difference"].std(),
            matched["Mass Difference"].min(),
            matched["Mass Difference"].max(),
            matched["Mass Difference"].quantile(0.25),
            matched["Mass Difference"].median(),
            matched["Mass Difference"].quantile(0.75),
        ]
    }
    stat_df = pd.DataFrame(stats)
    stat_df["Value (kg)"] = stat_df["Value (kg)"].map(lambda x: f"{x:.2f}")

    st.dataframe(stat_df, use_container_width=True, hide_index=True)


def render_analysis():
    """
    Load session state and render all analysis sections.
    """
    SessionStateManager.initialize()
    old_df = st.session_state.get("input_excel_old")
    new_df = st.session_state.get("input_excel_new")
    pta_type = st.session_state.get("pta_type")
    
    result_df = generate_results_df(old_df, new_df, pta_type)

    if result_df.empty:
        st.error("No data found. Please upload and process files first.")
        return

    render_overview(result_df)
    render_mass_distribution(result_df)
    render_change_type_distribution(result_df)
    render_summary_statistics(result_df)
