import logging
import requests
from datetime import datetime
import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL
logger = logging.getLogger(__name__)

SideBarLinks()

if st.button("⬅️ Go Back to User Home", use_container_width=True):
    st.switch_page('pages/User_Home.py')

# assuming user 4 is logged in
user_id = 4

st.title("Completed Workouts")
st.markdown("Log a workout you've completed and view your history!")

st.subheader("Add a Completed Workout")
if True:
    with st.form("completed_workout_form"):
        workout_id = st.text_input("Enter Workout ID")
        completed_at = st.date_input("Date Completed", value=datetime.today())
        notes = st.text_area("Notes (optional)")

        submitted = st.form_submit_button("Add Workout")
        if submitted:
            if workout_id.strip() == "":
                st.warning("Please enter a valid Workout ID.")
            else:
                payload = {
                    "workout_id": workout_id.strip(),
                    "completed_at": completed_at.strftime('%Y-%m-%d'),
                    "notes": notes
                }
                try:
                    response = requests.post(f"{API_URL}/f/completedWorkouts/{user_id}", json=payload)
                    if response.status_code == 200:
                        st.success("Workout logged successfully!")
                        st.rerun()
                    else:
                        error = response.json().get("error", "Failed to log workout.")
                        st.error(error)
                except Exception as e:
                    st.error(f"Error: {e}")


st.subheader("📋 Your Completed Workouts")
try:
    completed = requests.get(f"{API_URL}/f/completedWorkouts/{user_id}").json()
except:
    st.error("Could not load completed workouts.")
    completed = []

if completed:
    for i, entry in enumerate(completed):
        st.markdown(f"**Workout:** {entry['name']}  \n"
                    f"**Completed At:** {entry['completedAt']}  \n"
                    f"**Notes:** {entry['notes'] or '—'}")

        if st.button("🗑️ Delete", key=f"delete_{entry['workoutId']}_{i}"):
            try:
                del_response = requests.delete(f"{API_URL}/f/completedWorkouts/{user_id}", json={
                    "workout_id": entry["workoutId"]
                })
                if del_response.status_code == 200:
                    st.success("Workout deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete workout.")
            except Exception as e:
                st.error(f"Error: {e}")
        st.markdown("---")
