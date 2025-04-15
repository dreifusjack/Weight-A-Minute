import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL
logger = logging.getLogger(__name__)

if st.button("⬅️ Go Back to User Home", use_container_width=True):
    st.switch_page('pages/User_Home.py')

st.title('View A Gym Record Leaderboard')

# have the user input a gym id
gym_id = st.text_input("Enter Gym ID to View Leaderboard", help="e.g., 1, 5, 10")

if gym_id:
    try:
        response = requests.get(API_URL + f"c/gyms/{gym_id}/records")
        if response.status_code == 200:
            records = response.json()
            if not records:
                st.info("No records found for this gym.")
            else:
                st.header(f"Leaderboard for Gym ID: {gym_id}")
                for i, record in enumerate(records):
                    with st.expander(f"{record.get('name', 'N/A')} - User {record.get('userId', 'N/A')}"):
                        st.write(f"**Type:** {record.get('type', 'N/A')}")
                        st.write(f"**Weight:** {record.get('weight', 'N/A')} lbs")
                        st.write(f"**Reps:** {record.get('reps', 'N/A')}")
                        st.write(f"**Gym ID:** {record.get('gymId', 'N/A')}")
        else:
            st.error(f"Failed to fetch records. Status code: {response.status_code}")
    except Exception as e:
        st.error("Error fetching records: " + str(e))