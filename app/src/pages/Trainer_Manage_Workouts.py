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

st.title('My Workouts')

if 'trainerId' not in st.session_state:
    st.switch_page('Home.py')

trainerId = st.session_state['trainerId']

if 'exercise_edit_id' not in st.session_state:
    st.session_state.exercise_edit_id = None

def start_editing_exercise(id):
    st.session_state.exercise_edit_id = id


def deleteExercise(exerciseId):
    return

def editExercise(exerciseId, sets, reps):
    return

def workoutCard(workoutData, id):
    with st.container(height=300, border=False):
        cols = st.columns(2)
        for index, workout in enumerate(workoutData):
            with cols[index % 2]:
                name = workout.get("e.name", "Missing name")
                reps = workout.get("reps", "Missing reps")
                sets = workout.get("sets", "Missing sets")
                
                with st.container(border=True):
                    if st.session_state.exercise_edit_id == workout['exerciseId']:
                        st.markdown(f"**{name}**:")
                        exCol = st.columns([0.2, 0.2, 0.2, 0.1, 0.15, 0.15])
                        with exCol[0]:
                            new_sets = st.number_input(
                                "Sets", 
                                min_value=1, 
                                value=sets,
                                key=f"sets_{workout['exerciseId']}_{id}"
                            )
                        with exCol[1]:
                            st.markdown(f"**x**")
                        with exCol[2]:
                            new_reps = st.number_input(
                                "Reps", 
                                min_value=1, 
                                value=reps,
                                key=f"reps_{workout['exerciseId']}_{id}"
                            )
                        with exCol[4]:
                            if st.button("✅", key=f"save_{workout['exerciseId']}_{id}"):
                                editExercise(workout['exerciseId'], new_sets, new_reps)
                        with exCol[5]:
                            if st.button("❌", key=f"cancel_{workout['exerciseId']}_{id}"):
                                st.session_state.exercise_edit_id = None
                                st.rerun()
                    else:
                        exCol = st.columns([0.7, 0.15, 0.15])
                        with exCol[0]:
                            st.markdown(f"**{name}**:")
                            st.markdown(f"{sets} x {reps}")
                        with exCol[1]:
                            st.button(
                            "✏️", 
                            key=f"edit_{name}_{id}",
                            on_click=start_editing_exercise,
                            args=(workout['exerciseId'],),
                            )
                        
                        with exCol[2]:
                            st.button(
                            "🗑️", 
                            key=f"delete_{name}_{id}",
                            on_click=deleteExercise,
                            args=(workout['exerciseId'],),
                            )
                    


# Fetching workouts
try:
    workouts = requests.get(API_URL + f'/f/workouts/createdBy/{trainerId}').json()
except:
    st.error("Failed to load workouts.")
    workouts = []

for index, workout in enumerate(workouts):
    workoutId = workout.get("workoutId", "Missing id")
    workout_name = workout.get("name", "Missing name")
    workout_time = workout.get("time", "Missing time")
    workout_timesPerWeek = workout.get("TimesPerWeek", "Missing times per week")
    with st.container():
        st.markdown(f"**Name:** {workout_name}")
        st.markdown(f"**Time:** {workout_time}")
        st.markdown(f"**Target Times Per Week:** {workout_timesPerWeek}")
        st.markdown(f"**ID:** {workoutId}")
        with st.expander(f"View/Edit", expanded=False):
            aworkout = requests.get(API_URL + f'/f/workouts/{workoutId}').json()
            workoutCard(aworkout, workoutId)