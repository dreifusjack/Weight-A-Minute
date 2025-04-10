import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Add Admin Home Page')

if st.button('Update FAQs', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_View_FAQs.py')

if st.button('Gym Information', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_View_Gyms.py')

if st.button('User Information', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_ML_Model_Mgmt.py')