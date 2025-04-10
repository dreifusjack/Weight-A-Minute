import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

st.set_page_config(layout='wide')

SideBarLinks()

if st.button("⬅️ Go Back to Admin Home", use_container_width=True):
    st.switch_page('pages/Admin_Home.py')

st.title('Weight A Minute Gyms')

if st.button('Gym Requests', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/Admin_View_GymRequests.py')

# Fetching gyms
try:
    gyms = requests.get(API_URL + '/g/gyms').json()
except:
    st.error("Failed to load gyms.")
    gyms = []

if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

st.markdown("## Supported Gyms")
st.markdown("---")

# Rendering gyms as cards
for idx, gym in enumerate(gyms):
    gym_id = gym.get("gymId", "Missing id")
    gym_name = gym.get("name", "Missing name")
    gym_type = gym.get("type", "Missing type")
    price = gym.get("monthlyPrice", "Missing price")
    location = gym.get("location", "Missing location")
    owner_id = gym.get("ownerId", "Missing owner")

    try:
        owner = requests.get(API_URL + f'u/users/{owner_id}').json()
        name = f"{owner[0]['firstName']} {owner[0]['lastName']}"
    except:
        name = "Unknown Owner"

    with st.container():
        with st.expander(f"🏋️ **{gym_name}**", expanded=False):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Owner:** {name}")
                st.markdown(f"**Monthly Price:** ${price}")
                st.markdown(f"**Gym Type:** {gym_type}")
                st.markdown(f"**Location:** {location}")

            with col2:
                if st.session_state.delete_index == idx:
                    st.warning("Are you sure you want to remove this Gym?")
                    confirm_col, cancel_col = st.columns(2)
                    with confirm_col:
                        if st.button("Yes, removes", key=f"confirm_delete_{idx}"):
                            requests.delete(API_URL + f"g/gyms/{gym_id}")
                            st.session_state.delete_index = None
                            st.rerun()
                    with cancel_col:
                        if st.button("Cancel", key=f"cancel_delete_{idx}"):
                            st.session_state.delete_index = None
                            st.rerun()
                else:
                    if st.button("Remove", key=f"delete_btn_{idx}"):
                        st.session_state.delete_index = idx
                        st.rerun()

    st.markdown("---")
