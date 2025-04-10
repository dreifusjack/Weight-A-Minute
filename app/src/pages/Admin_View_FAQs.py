import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('FAQs')


# faqs = requests.get(API_URL + "c/faqs")

mock_data = [
    {'question': 'What is your return policy?', 'answer': 'You can return within 30 days.'},
    {'question': 'Do you offer international shipping?', 'answer': 'Yes, we ship worldwide.'},
    {'question': 'How can I contact support?', 'answer': 'Use the contact form or email us at support@example.com.'}
]

# state tracking for if a faq is being edited, deleted, or created
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None
if "delete_index" not in st.session_state:
    st.session_state.delete_index = None
if "creating_faq" not in st.session_state:
    st.session_state.creating_faq = None

# FAQ creation logic 
if st.button("Create FAQ"):
    st.session_state.creating_faq = True

if st.session_state.creating_faq:
    st.subheader("Create a New FAQ")
    new_question = st.text_input("New Question", key="new_q")
    new_answer = st.text_area("New Answer", key="new_a")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save (stub)"):
            st.info("This would send a POST request to create a new FAQ.")
            mock_data.append({"question": new_question, "answer": new_answer})  # Mocking the addition of the FAQ
            st.session_state.creating_faq = False
            st.session_state.edit_index = None
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state.creating_faq = False
            st.session_state.edit_index = None
            st.rerun()

st.markdown("---")

# FAQ rendering logic + updating
for idx, faq in enumerate(mock_data):
    if st.session_state.edit_index == idx:
        st.text_input("Edit Question", value=faq['question'], key=f"edit_q_{idx}", disabled=False)
        st.text_area("Edit Answer", value=faq['answer'], key=f"edit_a_{idx}", disabled=False)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Save (stub)", key=f"save_{idx}"):
                st.info("This would send an update to the API.")
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
            if st.button("Yes, delete (stub)", key=f"confirm_delete_{idx}"):
                st.info("This would send a delete request to the API.")
                st.session_state.delete_index = None
                st.rerun()
        with col2:
            if st.button("Cancel", key=f"cancel_delete_{idx}"):
                st.session_state.delete_index = None
                st.rerun()

    else:
        st.subheader(f"{idx + 1}: {faq['question']}")
        st.write(f"**Answer:** {faq['answer']}")
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