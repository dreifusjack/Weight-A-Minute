import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About Weight A Minute")

st.markdown (
    """
    👋 We're Weight a Miniute
A fitness app built to make your workouts smarter, not harder.

🏋️ Personalized Workouts
No more one-size-fits-all plans — we tailor your workouts to the equipment at your gym.

📈 Track Your Progress
Log workouts, stay on track, and crush your goals.

🤝 Connect with Trainers
Get feedback and guidance — no awkward scheduling needed.

🏢 Gym Owners Welcome
Show off your gym! Add your location, equipment list, and more.

💡 Why it matters:
Not all gyms are the same. We make sure your workout actually works wherever you are.
    """
        )
