import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL
logger = logging.getLogger(__name__)


if st.button("⬅️ Go Back to User Home", use_container_width=True):
    st.switch_page('pages/User_Home.py')

st.title("Submit an FAQ Question")

st.markdown("Have a question? Submit it and we'll will review it for the FAQ!")

# submission form
with st.form("submit_faq_form"):
    question = st.text_area("Your Question", help="Type your question here...")
    email = st.text_input("Your Email (optional)", help="We might want to follow up")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not question.strip():
            st.warning("Please enter a question before submitting.")
        else:
            payload = {
                "question": question,
                "answer": "",
                "submittedBy": email if email else "Anonymous"
            }
            try:
                response = requests.post(API_URL + "u/faqs", json=payload)
                if response.status_code == 200:
                    st.success("Thanks! Your question has been submitted.")
                else:
                    st.error(f"Submission failed. Status code: {response.status_code}")
            except Exception as e:
                st.error("Something went wrong: " + str(e))

