import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL
logger = logging.getLogger(__name__)

SideBarLinks()

if st.button("⬅️ Go Back to User Home", use_container_width=True):
    st.switch_page('pages/User_Home.py')

st.title("Frequently Asked Questions")


# Fetching faqs
try:
    faqs = requests.get(API_URL + '/u/faqs').json()
except:
    st.error("Failed to load FAQs.")
    faqs = []



st.markdown("---")

# faq rendering logic + updating
for idx, faq in enumerate(faqs):
    question = faq.get("question", "Missing question")
    answer = faq.get("answer", "Missing answer")
    st.subheader(f"{idx + 1}: {question}")
    st.write(f"**Answer:** {answer}")

    st.markdown("---")