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

st.title('Weight A Minute Users')

# Fetching users
try:
    users = requests.get(API_URL + '/u/users').json()
except:
    st.error("Failed to load users.")
    users = []


# Logic to send email notifications 
st.markdown("## Send Notification to All Users")

if "reset_form" in st.session_state and st.session_state.reset_form:
    st.session_state.subject_input = ""
    st.session_state.body_input = ""
    st.session_state.reset_form = False
    st.rerun() 

if "subject_input" not in st.session_state:
    st.session_state.subject_input = ""
if "body_input" not in st.session_state:
    st.session_state.body_input = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# Email form
with st.form("email_notification_form"):
    st.text_input("Subject", key="subject_input")
    st.text_area("Message Body", height=150, key="body_input")
    submitted = st.form_submit_button("Send Email")

    if submitted:
        subject = st.session_state.subject_input
        body = st.session_state.body_input

        if not subject or not body:
            st.warning("Please fill out both the subject and body fields.")
        else:
            payload = {
                "subject": subject,
                "body": body
            }
            response = requests.post(API_URL + "u/users/notification", json=payload)
            if response.status_code == 200:
                st.session_state.reset_form = True 
                st.rerun()
                st.success("Notification sent successfully!")
            else:
                st.error(f"Failed to send notification. Status code: {response.status_code}")



st.markdown("---")
st.markdown("## Current users")
st.markdown("---")

if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

# Rendering users as cards
for idx, user in enumerate(users):
    user_id = user.get("userId", "Missing id")
    user_name = user.get("firstName", "Missing first name") + " " + user.get("lastName", "Missing last name")
    dob = user.get("DOB", "Missing DOB")
    gender = user.get("gender", "Missing gender")
    email = user.get("email", "Missing emails")

    with st.container():
        with st.expander(f"🤠 **{user_name}**", expanded=False):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Name:** {user_name}")
                st.markdown(f"**Date of Brith:** {dob}")
                st.markdown(f"**Gender:** {gender}")
                st.markdown(f"**Email:** {email}")

            with col2:
                if st.session_state.delete_index == idx:
                    st.warning("Are you sure you want to deactivate this user?")
                    confirm_col, cancel_col = st.columns(2)
                    with confirm_col:
                        if st.button("Yes, remove", key=f"confirm_delete_{idx}"):
                            requests.delete(API_URL + f"u/users/{user_id}")
                            st.session_state.delete_index = None
                            st.rerun()
                    with cancel_col:
                        if st.button("Cancel", key=f"cancel_delete_{idx}"):
                            st.session_state.delete_index = None
                            st.rerun()
                else:
                    if st.button("Deactivate", key=f"delete_btn_{idx}"):
                        st.session_state.delete_index = idx
                        st.rerun()

    st.markdown("---")
