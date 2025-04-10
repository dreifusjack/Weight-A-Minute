import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

st.set_page_config(layout = 'wide')

SideBarLinks()

if st.button("⬅️ Go Back to Admin Home", use_container_width=True):
    st.switch_page('pages/Admin_Home.py')

st.title('FAQs')

# Fetching faqs
try:
    faqs = requests.get(API_URL + '/u/faqs').json()
except:
    st.error("Failed to load FAQs.")
    faqs = []

# state tracking for if a faq is being edited, deleted, or created
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None
if "delete_index" not in st.session_state:
    st.session_state.delete_index = None
if "creating_faq" not in st.session_state:
    st.session_state.creating_faq = None

# faq creation logic 
if st.button("Create FAQ"):
    st.session_state.creating_faq = True

if st.session_state.creating_faq:
    st.subheader("Create a New FAQ")
    new_q = st.text_input("New Question", key="new_q")
    new_a = st.text_area("New Answer", key="new_a")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save"):
            payload = {
                "question":  new_q,
                "answer": new_a
            }
            requests.post(API_URL + "u/faqs", json=payload)
            st.session_state.creating_faq = None
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state.creating_faq = None
            st.rerun()

st.markdown("---")

# faq rendering logic + updating
for idx, faq in enumerate(faqs):
    question = faq.get("question", "Missing question")
    answer = faq.get("answer", "Missing answer")
    faq_id = faq.get("faqId", "Missing id")
    
    if st.session_state.edit_index == idx:
        updated_q = st.text_input("Edit Question", value=question, key=f"edit_q_{idx}", disabled=False)
        updated_a = st.text_area("Edit Answer", value=answer, key=f"edit_a_{idx}", disabled=False)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Save", key=f"save_{idx}"):
                payload = {
                    "question": updated_q,
                    "answer": updated_a
                }
                requests.put(API_URL + f"u/faqs/{faq_id}", json=payload)
                st.session_state.edit_index = None
                st.rerun()
        with col2:
            if st.button(" Cancel", key=f"cancel_edit_{idx}"):
                st.session_state.edit_index = None
                st.rerun()

    elif st.session_state.delete_index == idx:
        st.warning(" Are you sure you want to delete this FAQ? This cannot be undone.")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Yes, delete", key=f"confirm_delete_{idx}"):
                requests.delete(API_URL + f"u/faqs/{faq_id}")
                st.session_state.delete_index = None
                st.rerun()
        with col2:
            if st.button("Cancel", key=f"cancel_delete_{idx}"):
                st.session_state.delete_index = None
                st.rerun()

    else:
        st.subheader(f"{idx + 1}: {question}")
        st.write(f"**Answer:** {answer}")
        col1, col2 = st.columns([1, 1])
        with col1:  
            if st.button("Edit", key=f"edit_btn_{idx}"):
                st.session_state.edit_index = idx
                st.session_state.delete_index = None
                st.rerun()
        with col2:
            if st.button("Delete", key=f"delete_btn_{idx}"):
                st.session_state.delete_index = idx
                st.session_state.edit_index = None
                st.rerun()

    st.markdown("---")