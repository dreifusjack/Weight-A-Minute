import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Add Owner Home Page')

if st.button('Create A Gym Request', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Owner_Gym_Request.py')

if st.button('Manage Gym Subscriptions', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Owner_Manage_Subscriptions.py')

if st.button('Manage Gym Leaderboards', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Owner_Manage_Leaderboard.py')