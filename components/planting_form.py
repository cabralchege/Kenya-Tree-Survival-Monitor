import streamlit as st
import sqlite3
from datetime import date

def show():
    st.title("🌱 Record New Planting")
    
    with st.form("planting_form"):
        species = st.selectbox(
            "Tree Species",
            ["Mango", "Cedar", "Bamboo", "Acacia", "Grevillea", "Other"]
        )
        
        quantity = st.number_input("Number of Trees", min_value=1, value=100)
        
        location = st.text_input("Planting Location", placeholder="e.g., Nairobi - Site A")
        
        date_planted = st.date_input("Planting Date", value=date.today())
        
        season = st.selectbox("Season", ["Rainy", "Dry"])
        
        notes = st.text_area("Additional Notes (optional)")
        
        submitted = st.form_submit_button("Save Planting Record")
        
        if submitted:
            # Save to database
            conn = sqlite3.connect('forest_impact.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO plantings (species, quantity, location, date_planted, season, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (species, quantity, location, date_planted, season, notes))
            conn.commit()
            planting_id = cursor.lastrowid
            conn.close()
            
            st.success(f"✅ Planting recorded! Batch ID: #{planting_id}")
            st.balloons()