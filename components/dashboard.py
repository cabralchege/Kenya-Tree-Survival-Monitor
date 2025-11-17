import streamlit as st
import plotly.express as px
import pandas as pd
from utils.calculations import get_survival_by_species

def show():
    st.title("🌳 ForestImpact Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trees Planted", "5,000")
    with col2:
        st.metric("Overall Survival Rate", "84%", "+3%")
    with col3:
        st.metric("Active Projects", "12")
    with col4:
        st.metric("CO2 Offset (tons)", "180")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Survival Rate by Species")
        # Sample data - replace with real database query
        data = pd.DataFrame({
            'Species': ['Mango', 'Cedar', 'Bamboo', 'Acacia'],
            'Survival Rate': [85, 78, 92, 73]
        })
        fig = px.bar(data, x='Species', y='Survival Rate', 
                     color='Survival Rate',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("📈 Survival Trend Over Time")
        # Time series chart
        trend_data = pd.DataFrame({
            'Month': ['Aug', 'Sep', 'Oct', 'Nov'],
            'Survival Rate': [80, 82, 83, 84]
        })
        fig = px.line(trend_data, x='Month', y='Survival Rate', 
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)