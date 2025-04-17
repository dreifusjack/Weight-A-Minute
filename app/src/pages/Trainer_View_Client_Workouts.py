import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

st.set_page_config(layout='wide')

SideBarLinks()

if st.button("⬅️ Go Back to Trainer Home"):
    st.switch_page('pages/Personal_Trainer_Home.py')

st.title('My Clients')

if 'trainerId' not in st.session_state:
    st.switch_page('Home.py')

trainerId = st.session_state['trainerId']

# Fetching users
try:
    clients = requests.get(API_URL + f'/u/trainer/clients/{trainerId}').json()
except:
    st.error("Failed to load users.")
    clients = []


def workoutCard(workoutData):
    with st.container(height=300, border=False):
        cols = st.columns(2)
        for index, workout in enumerate(workoutData):
            with cols[index % 2]:
                completed_At = workout.get("completedAt", "Missing completion date")
                workout_name = workout.get("name", "Missing name")
                workout_notes = workout.get("notes", "Missing notes")
                
                with st.container(border=True):
                    st.markdown(f"**{workout_name}** 🕒 {completed_At}")
                    st.markdown(f"**Notes:** {workout_notes}")

                st.write("")

for index, user in enumerate(clients):
    user_id = user.get("userId", "Missing id")
    user_name = user.get("firstName", "Missing first name") + " " + user.get("lastName", "Missing last name")
    dob = user.get("DOB", "Missing DOB")
    gender = user.get("gender", "Missing gender")
    email = user.get("email", "Missing emails")
    with st.container():
        with st.expander(f"**{user_name}**", expanded=False):
            try:
                userWorkouts = requests.get(API_URL + f'/f/completedWorkouts/{user_id}').json()
                workoutCard(userWorkouts)
            except:
                st.error("Failed to load a user's workouts")
                clients = []
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Date of Brith:** {dob}")
                st.markdown(f"**Gender:** {gender}")
                st.markdown(f"**Email:** {email}")
