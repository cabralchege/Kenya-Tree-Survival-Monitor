import streamlit as st
import sqlite3
from datetime import date

def show():
    st.title("📋 Record Survival Check")
    
    # First, get list of existing plantings to check
    conn = sqlite3.connect('forest_impact.db')
    cursor = conn.cursor()
    
    plantings = cursor.execute('''
        SELECT id, species, quantity, location, date_planted 
        FROM plantings 
        ORDER BY date_planted DESC
    ''').fetchall()
    
    conn.close()
    
    if not plantings:
        st.warning("⚠️ No plantings recorded yet. Please record a planting first.")
        if st.button("Go to Record Planting"):
            st.switch_page("Record Planting")
        return
    
    # Display plantings as options
    st.subheader("Select Planting Batch to Check")
    
    planting_options = []
    for p in plantings:
        planting_id, species, quantity, location, date_planted = p
        option_text = f"Batch #{planting_id}: {quantity} {species} trees - {location} (Planted: {date_planted})"
        planting_options.append((planting_id, option_text))
    
    selected_option = st.selectbox(
        "Choose planting batch",
        options=[opt[1] for opt in planting_options]
    )
    
    # Get selected planting ID
    selected_id = None
    for planting_id, option_text in planting_options:
        if option_text == selected_option:
            selected_id = planting_id
            break
    
    # Get planting details
    conn = sqlite3.connect('forest_impact.db')
    cursor = conn.cursor()
    planting = cursor.execute('''
        SELECT species, quantity, location, date_planted 
        FROM plantings 
        WHERE id = ?
    ''', (selected_id,)).fetchone()
    conn.close()
    
    species, total_planted, location, date_planted = planting
    
    # Show planting info
    st.info(f"""
    **Batch Details:**
    - Species: {species}
    - Trees Planted: {total_planted}
    - Location: {location}
    - Date Planted: {date_planted}
    """)
    
    st.divider()
    
    # Survival check form
    st.subheader("Record Survival Status")
    
    with st.form("survival_check_form"):
        check_date = st.date_input("Check Date", value=date.today())
        
        alive_count = st.number_input(
            "Number of Trees Alive", 
            min_value=0, 
            max_value=total_planted,
            value=total_planted
        )
        
        # Auto-calculate dead
        dead_count = total_planted - alive_count
        st.metric("Trees Dead/Missing", dead_count)
        
        # Calculate survival rate
        survival_rate = round((alive_count / total_planted) * 100, 2) if total_planted > 0 else 0
        st.metric("Survival Rate", f"{survival_rate}%")
        
        health_notes = st.text_area(
            "Health Observations (optional)",
            placeholder="E.g., Some trees showing signs of drought stress, pest damage observed..."
        )
        
        submitted = st.form_submit_button("Save Survival Check")
        
        if submitted:
            # Save to database
            conn = sqlite3.connect('forest_impact.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO survival_checks 
                (planting_id, check_date, alive_count, dead_count, health_notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (selected_id, check_date, alive_count, dead_count, health_notes))
            conn.commit()
            check_id = cursor.lastrowid
            conn.close()
            
            # Success message with insights
            st.success(f"✅ Survival check recorded! Check ID: #{check_id}")
            
            # Show status with color
            if survival_rate >= 85:
                st.success(f"🌟 Excellent! {survival_rate}% survival rate is above average.")
            elif survival_rate >= 70:
                st.info(f"👍 Good! {survival_rate}% survival rate is acceptable.")
            elif survival_rate >= 50:
                st.warning(f"⚠️ Fair. {survival_rate}% survival rate could be improved.")
            else:
                st.error(f"🚨 Low survival rate ({survival_rate}%). Investigation recommended.")
            
            st.balloons()
    
    st.divider()
    
    # Show previous checks for this planting (if any)
    st.subheader("📊 Previous Checks for This Batch")
    
    conn = sqlite3.connect('forest_impact.db')
    cursor = conn.cursor()
    previous_checks = cursor.execute('''
        SELECT check_date, alive_count, dead_count, health_notes
        FROM survival_checks
        WHERE planting_id = ?
        ORDER BY check_date DESC
    ''', (selected_id,)).fetchall()
    conn.close()
    
    if previous_checks:
        for check in previous_checks:
            check_date, alive, dead, notes = check
            survival = round((alive / total_planted) * 100, 2) if total_planted > 0 else 0
            
            with st.expander(f"Check on {check_date} - {survival}% survival"):
                st.write(f"**Alive:** {alive} | **Dead:** {dead}")
                if notes:
                    st.write(f"**Notes:** {notes}")
    else:
        st.info("No previous checks recorded for this batch.")