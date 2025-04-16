import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

logger = logging.getLogger(__name__)

SideBarLinks()

if st.button("⬅️ Go Back to Owner Home", use_container_width=True):
    st.switch_page('pages/Owner_Home.py')

st.title("Manage Gym Leaderboards")

gym_id = 1

st.header("Add New Leaderboard Record")

with st.form("add_record_form"):
    user_id = st.text_input("User ID", help="e.g., 1, 10, 500")
    name = st.text_input("Record Name", help="e.g., Bench Press")
    record_type = st.text_input("Type", help="e.g., Chest, Legs, Back")
    weight = st.number_input("Weight (lbs)", min_value=1)
    reps = st.number_input("Repetitions", min_value=1)

    submitted = st.form_submit_button("Add Record")

    if submitted:
        if not user_id or not name or not record_type:
            st.warning("Please fill in all required fields.")
        else:
            payload = {
                "userId": int(user_id),
                "name": name,
                "type": record_type,
                "weight": int(weight),
                "reps": int(reps)
            }
            response = requests.post(API_URL + f"c/gyms/{gym_id}/records", json=payload)
            if response.status_code == 200:
                st.rerun()
                st.success("Record added successfully!")
            else:
                st.error(f"Failed to add record. Status code: {response.status_code}")

st.header("Current Leaderboard Records")

try:
    response = requests.get(API_URL + f"c/gyms/{gym_id}/records")
    if response.status_code == 200:
        records = response.json()
    else:
        st.error(f"Failed to fetch records. Status code: {response.status_code}")
        records = []
except Exception as e:
    st.error("Error fetching records: " + str(e))
    records = []

if records:
    for i, record in enumerate(records):
        user_id = (record.get('userId', 'N/A'))

        user = requests.get(API_URL + f'u/users/{user_id}').json()

        name = f"{user[0]['firstName']} {user[0]['lastName']}"
        st.write(f"**Member:** {name}")
        st.write(f"**Record Name:** {record.get('name', 'N/A')}")
        st.write(f"**Type:** {record.get('type', 'N/A')}")
        st.write(f"**Weight:** {record.get('weight', 'N/A')}")
        st.write(f"**Reps:** {record.get('reps', 'N/A')}")
        st.write(f"**Gym ID:** {record.get('gymId', 'N/A')}")
        
        if st.button("Remove Record", key=f"delete_{record.get('name', '')}_{i}"):
            payload = {
                "userId": record.get('userId'),
                "name": record.get('name')
            }

            del_response = requests.delete(API_URL + f"c/gyms/{gym_id}/records", json=payload)

            if del_response.status_code == 200:
                st.rerun()
                st.success("Record deleted successfully!")
            else:
                st.error(f"Failed to delete record. Status code: {del_response.status_code}")

        st.markdown("---")
else:
    st.info("No leaderboard records found.")