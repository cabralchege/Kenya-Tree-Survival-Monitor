import streamlit as st
from components import dashboard, planting_form, survival_check

st.set_page_config(
    page_title="ForestImpact Tracker",
    page_icon="🌳",
    layout="wide"
)

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Record Planting", "Track Survival", "AI Predictions", "Reports"]
)

# Page routing
if page == "Dashboard":
    dashboard.show()
elif page == "Record Planting":
    planting_form.show()
elif page == "Track Survival":
    survival_check.show()
elif page == "AI Predictions":
    st.title("🤖 AI Survival Predictor")
    # AI prediction interface
elif page == "Reports":
    st.title("📄 Generate Reports")
    # Report generation interface