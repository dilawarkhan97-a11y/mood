import os

import streamlit as st

st.set_page_config(page_title="Daily Mood Tracker", page_icon="😄", layout="centered")

st.title("🌤️ Daily Productivity & Mood Tracker")

tasks = [
    "Eat x2", "Code", "Hot tub", "Swimming", "Ice cream", "Game", "TV",
    "Read", "Write", "Drive", "Park", "Clean", "Cook",
    "Protein", "Skin care", "Exercise", "Family/Friends"
]

POINTS_PER_TASK = 25
PRAYER_BONUS = 25

st.write("Check everything you did today:")
checks = {t: st.checkbox(t) for t in tasks}
prayers = st.number_input("How many times did you pray today?", 0, 50, 0)

score = sum(checks.values()) * POINTS_PER_TASK + prayers * PRAYER_BONUS

if score <= 200:
    mood = "Awful 😞"
elif score <= 300:
    mood = "Bad 😔"
elif score <= 400:
    mood = "Normal 😐"
elif score <= 500:
    mood = "Good 🙂"
else:
    mood = "Great 😄"

st.subheader(f"**Score:** {score}")
st.subheader(f"**Mood:** {mood}")

