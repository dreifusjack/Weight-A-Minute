import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

SideBarLinks()

if st.button("⬅️ Go Back to Owner Home", use_container_width=True):
    st.switch_page('pages/Owner_Home.py')

st.title('Create A Gym Request')

if "reset_form" in st.session_state and st.session_state.reset_form:
    st.session_state.request_details = ""
    st.session_state.reset_form = False
    st.rerun() 

if "request_details" not in st.session_state:
    st.session_state.request_details = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# Email form
with st.form("email_notification_form"):
    st.text_area("Gym Details", height=150, key="request_details")
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        details = st.session_state.request_details

        if not details:
            st.warning("Please fill out the request details.")
        else:
            payload = {
                "details": details
            }
            response = requests.post(API_URL + "g/gymRequests", json=payload)
            if response.status_code == 200:
                st.session_state.reset_form = True 
                st.success("Gym request sent successfully!")
            else:
                st.error(f"Failed to send gym request. Status code: {response.status_code}")