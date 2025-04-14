import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

logger = logging.getLogger(__name__)

if st.button("⬅️ Go Back to Owner Home", use_container_width=True):
    st.switch_page('pages/Owner_Home.py')

st.title("Manage Gym Subscriptions")

gym_id = 1

st.header("Current Gym Subscriptions")

try:
    response = requests.get(API_URL + f"c/gyms/{gym_id}/subscriptions")
    if response.status_code == 200:
        subscriptions = response.json()
    else:
        st.error(f"Failed to fetch subscriptions. Status code: {response.status_code}")
        subscriptions = []
except Exception as e:
    st.error("Error fetching subscriptions: " + str(e))
    subscriptions = []

if subscriptions:
    for i, subscription in enumerate(subscriptions):
        st.write(f"**Subscription ID:** {subscription.get('subscriptionId')}")
        st.write(f"**User ID:** {subscription.get('userId')}")
        st.write(f"**Tier:** {subscription.get('tier')}")
        st.write(f"**Monthly Fee:** {subscription.get('monthlyFee')}")
        st.write(f"**Length:** {subscription.get('length')}")
        
        if st.button("Cancel Subscription", key=f"cancel_{subscription.get('subscriptionId', '')}_{i}"):
            payload = {"subscriptionId": subscription.get("subscriptionId")}
            del_response = requests.delete(API_URL + f"c/gyms/{gym_id}/subscriptions", json=payload)
            
            if del_response.status_code == 200:
                st.rerun()
                st.success("Subscription canceled successfully!")
            else:
                st.error(f"Failed to cancel subscription. Status code: {del_response.status_code}")
        st.markdown("---")
else:
    st.info("No subscriptions found.")
