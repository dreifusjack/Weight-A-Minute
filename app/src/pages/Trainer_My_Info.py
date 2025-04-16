import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from shared.api_url import API_URL

st.set_page_config(layout='wide')

SideBarLinks()

if st.button("⬅️ Go Back to Admin Home"):
    st.switch_page('pages/Personal_Trainer_Home.py')

st.title('My Info')

if 'trainerId' not in st.session_state:
    st.switch_page('Home.py')

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

trainerId = st.session_state['trainerId']

trainer = requests.get(API_URL + f'/u/trainer/{trainerId}').json()[0]
trainerType = trainer.get("type", "missing type")
try:
    trainerYOE = int(trainer.get("YOE", 0))
except (ValueError, TypeError):
    trainerYOE = 0
trainerDesc = trainer.get("description", "missing description")

def updateInfo(type, yoe, description):
    try: 
        payload = {
            "type": type,
            "YOE": yoe,
            "description": description
        }
        requests.put(API_URL + f'/u/trainer/{trainerId}', json=payload)
        st.session_state.edit_mode = False
        st.rerun()
    except Exception as e:
        st.error(f"Failed to change exercise in workout: {e}")

with st.container():
    col1, col2 = st.columns([3, 1])
    
    # Display mode (default)
    if not st.session_state.edit_mode:
        with col1:
            st.subheader(trainerType)
            st.write(f"Years of Experience: {trainerYOE}")
            st.write(f"Description: {trainerDesc}")
        
        with col2:
            if st.button("Edit Profile"):
                st.session_state.edit_mode = True
                st.rerun()
    
    # Edit mode
    else:
        with col1:
            # Form for editing
            with st.form(key="edit_profile_form"):
                new_type = st.text_input("Type of Trainer", value=trainerType)
                new_years = st.number_input("Years of Experience", 
                                            min_value=0, 
                                            value=trainerYOE)
                new_description = st.text_area("Description", 
                                                value=trainerDesc)
                
                col1a, col1b = st.columns(2)
                with col1a:
                    if st.form_submit_button("Save"):
                        updateInfo(new_type, new_years, new_description)
                
                with col1b:
                    if st.form_submit_button("Cancel"):
                        st.session_state.edit_mode = False
                        st.rerun()