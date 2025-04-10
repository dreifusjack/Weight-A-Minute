import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

st.set_page_config(layout = 'wide')

SideBarLinks()

if st.button("⬅️ Go Back to Gyms", use_container_width=True):
    st.switch_page('pages/Admin_View_Gyms.py')

st.title('Requests To Review')

# Fetching requests
try:
    gym_requests = requests.get(API_URL + '/g/gymRequests').json()
except:
    st.error("Failed to load GymRequests.")
    gym_requests = []

# state tracking for if a request is being accepted or rejected
if "accept_index" not in st.session_state:
    st.session_state.accept_index = None
if "reject_index" not in st.session_state:
    st.session_state.reject_index = None

st.markdown("---")

# request rendering logic + updating
for idx, request in enumerate(gym_requests):
    req_date = request.get("requestDate", "Missing date")
    details = request.get("gymDetails", "Missing details")
    request_id = request.get("requestId", "Missing id")
    requester_id = request.get("userId", "Missing id")
    user = requests.get(API_URL + f"/u/users/{requester_id}").json()
    name = user[0]["firstName"]
    name = name + " " + user[0]["lastName"]
    
    if st.session_state.accept_index == idx:
        # updated_q = st.text_input("Edit Question", value=question, key=f"edit_q_{idx}", disabled=False)
        # updated_a = st.text_area("Edit Answer", value=answer, key=f"edit_a_{idx}", disabled=False)
        #TODO: come back if we want to create gyms here 
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Save", key=f"save_{idx}"):
                # payload = {
                #     "question": updated_q,
                #     "answer": updated_a
                # }
                # requests.put(API_URL + f"u/gym_requests/{faq_id}", json=payload)
                requests.delete(API_URL + f"g/gymRequests/{request_id}")
                st.session_state.accept_index = None
                st.rerun()
        with col2:
            if st.button(" Cancel", key=f"cancel_edit_{idx}"):
                st.session_state.accept_index = None
                st.rerun()

    elif st.session_state.reject_index == idx:
        st.warning(" Are you sure you want to reject this request? This cannot be undone.")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Yes, reject", key=f"confirm_delete_{idx}"):
                requests.delete(API_URL + f"g/gymRequests/{request_id}")
                st.session_state.reject_index = None
                st.rerun()
        with col2:
            if st.button("Cancel", key=f"cancel_delete_{idx}"):
                st.session_state.reject_index = None
                st.rerun()

    else:
        st.subheader("Request " +  f"{idx + 1}")
        st.write(f"**Request:** {details}")
        st.write(f"**Requested By:** {name}")
        st.write(f"**Requested On:** {req_date}")
        col1, col2 = st.columns([1, 1])
        with col1:  
            if st.button("Accept", key=f"edit_btn_{idx}"):
                st.session_state.accept_index = idx
                st.session_state.reject_index = None
                st.rerun()
        with col2:
            if st.button("Reject", key=f"delete_btn_{idx}"):
                st.session_state.reject_index = idx
                st.session_state.accept_index = None
                st.rerun()

    st.markdown("---")