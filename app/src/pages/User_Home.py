import logging
import streamlit as st
from modules.nav import SideBarLinks
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Welcome to the User Home Page!')

if st.button("⬅️ Go Back to Main Home", use_container_width=True):
    st.switch_page('Home.py')

if st.button('View a Gym Leaderboard📊',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/User_View_Leaderboard.py')

if st.button('Create an FAQ🙋',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/User_Create_FAQ.py')

if st.button('Edit a Completed Workout🏋️‍♂️',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/User_Edit_Completed_Workout.py')
