import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Personal Trainer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button("View My Clients",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Trainer_View_Client_Workouts.py')

if st.button("Manage My Workouts",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Trainer_Manage_Workouts.py')

if st.button("Manage My Info",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Trainer_My_Info.py')