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

allExercises = requests.get(API_URL + f'/g/exercises').json()
exerciseNames = [item["name"] for item in allExercises]
name_to_id = {item["name"]: item["exerciseId"] for item in allExercises}

def start_editing_exercise(workoutId, exerciseid):
    st.session_state.exercise_edit_id = f"{workoutId}_{exerciseid}"

def addExercise(workoutId, exerciseId, sets, reps):
    try: 
        payload = {
            "sets": sets,
            "reps": reps
        }
        requests.post(API_URL + f'/f/workouts/{workoutId}/{exerciseId}', json=payload)
        st.session_state.exercise_edit_id = None
        st.rerun()
    except Exception as e:
        st.error(f"Failed to change exercise in workout: {e}")

def deleteExercise(workoutId, exerciseId):
    try:
        requests.delete(API_URL + f'/f/workouts/{workoutId}/{exerciseId}')
    except Exception as e:
        st.error(f"Failed to delete exercise in workout: {e}")

def editExercise(workoutId, exerciseId, sets, reps):
    try: 
        payload = {
            "sets": sets,
            "reps": reps
        }
        requests.put(API_URL + f'/f/workouts/{workoutId}/{exerciseId}', json=payload)
        st.session_state.exercise_edit_id = None
        st.rerun()
    except Exception as e:
        st.error(f"Failed to change exercise in workout: {e}")

def createNewWorkout(name, timesPerWeek):
    try: 
        payload = {
            "name": name,
            "time": "12:00:00",
            "times_per_week": timesPerWeek
        }
        requests.post(API_URL + f'/f/workouts/createdBy/{trainerId}', json=payload)
        st.rerun()
    except Exception as e:
        st.error(f"Failed to change exercise in workout: {e}")

def workoutCard(workoutData, id):
    with st.container(height=300, border=False):
        cols = st.columns(2)
        for index, workout in enumerate(workoutData):
            with cols[index % 2]:
                name = workout.get("e.name", "Missing name")
                reps = workout.get("reps", "Missing reps")
                sets = workout.get("sets", "Missing sets")
                
                with st.container(border=True):
                    if st.session_state.exercise_edit_id == f"{id}_{workout['exerciseId']}":
                        st.markdown(f"**{name}**:")
                        exCol = st.columns([0.2, 0.2, 0.2, 0.1, 0.15, 0.15])
                        with exCol[0]:
                            new_sets = st.number_input(
                                "Sets", 
                                min_value=1, 
                                value=sets,
                                key=f"sets_{workout['exerciseId']}_{id}_{index}"
                            )
                        with exCol[1]:
                            st.markdown(f"**x**")
                        with exCol[2]:
                            new_reps = st.number_input(
                                "Reps", 
                                min_value=1, 
                                value=reps,
                                key=f"reps_{workout['exerciseId']}_{id}_{index}"
                            )
                        with exCol[4]:
                            if st.button("✅", key=f"save_{workout['exerciseId']}_{id}_{index}"):
                                editExercise(id, workout['exerciseId'], new_sets, new_reps)
                        with exCol[5]:
                            if st.button("❌", key=f"cancel_{workout['exerciseId']}_{id}_{index}"):
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
                            key=f"edit_{name}_{id}_{index}",
                            on_click=start_editing_exercise,
                            args=(id, workout['exerciseId'],),
                            )
                        
                        with exCol[2]:
                            st.button(
                            "🗑️", 
                            key=f"delete_{name}_{id}_{index}",
                            on_click=deleteExercise,
                            args=(id, workout['exerciseId'],),
                            )
        with cols[len(workoutData) % 2]:
            selected_exercise = st.selectbox(
                "Add an Exercise",
                options=exerciseNames,
                key=f"addToWorkout{id}"
            )
            createCol = st.columns([.3, .2, .3, .2])
            with createCol[0]:
                create_new_sets = st.number_input(
                    "Sets", 
                    min_value=1,
                    key=f"sets_{name_to_id[selected_exercise]}_{id}_create"
                )
            with createCol[1]:
                st.markdown(f"**x**")
            with createCol[2]:
                create_new_reps = st.number_input(
                    "Reps", 
                    min_value=1,
                    key=f"reps_{name_to_id[selected_exercise]}_{id}_create"
                )
            with createCol[3]:
                if st.button("✅", key=f"addnewexerpciseto_{id}"):
                    addExercise(id, name_to_id[selected_exercise], create_new_sets, create_new_reps)

                    


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
    with st.container(border=True):
        st.markdown(f"**Name:** {workout_name}")
        st.markdown(f"**Target Times Per Week:** {workout_timesPerWeek}")
        with st.container():
            aworkout = requests.get(API_URL + f'/f/workouts/{workoutId}').json()
            workoutCard(aworkout, workoutId)

with st.container(border=True):
    st.markdown("Create a New Workout")
    createForm = st.columns([.33, .33, .34])
    with createForm[0]:
        name = st.text_input("Name")
    with createForm[1]:
        timesPerWeek = st.number_input("Target Times Per Week", min_value=1)
    with createForm[2]:
        if st.button("Create"):
            if name:
                createNewWorkout(name, timesPerWeek)