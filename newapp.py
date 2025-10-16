import streamlit as st
import pandas as pd
import datetime as dt
import io
from datetime import datetime, timedelta
st.set_page_config(page_title="My First App", page_icon="📈", layout="centered")
st.title("📈 My first app")

# ---------- TABS ----------
tab_weekly, tab_daily ,tab_travel= st.tabs(["📅 Weekly Overview", "🌤️ Daily Tracker", "✈️ Travel"])

# ---------- WEEKLY TAB ----------
with tab_weekly:
    st.subheader("Weekly Productivity")

    # Data
    prod_per = [27, 65, 69, 71, 65, 70, 68, 63, 40, 55]
    prod_ave = [130, 300, 310, 321, 292, 317, 307, 282, 182, 250]
    weeks = [f"Week {i+1}" for i in range(len(prod_per))]
    start_date=datetime(25,8,6)
    Dates = [(start_date + timedelta(weeks=i)).strftime("%b %d, %Y") for i in range(len(prod_ave))]

    df = pd.DataFrame({"Week": weeks,
                       "Productivity (%)": prod_per,
                       "Average Output": prod_ave,
                       "Dates": Dates})

    st.dataframe(df, use_container_width=True)
    st.line_chart(df.set_index("Week")[["Productivity (%)", "Average Output"]])

# ---------- DAILY TAB ----------
with tab_daily:
    st.subheader("Daily Productivity & Mood Tracker")

    # --- Config ---

    POINTS_PER_TASK = 25
    PRAYER_BONUS = 25
    tasks = [
        "Eat x2 "
    "Code 💻",
    "Hot tub 🛁",
    "Swimming 🏊",
    "Ice cream 🍦",
    "Game",
    "TV 📺",
    "Read 📖",
    "Write ✍️",
    "Drive 🚗",
    "Park 🏞️",
    "Clean 🧹",
    "Cook 🍳",
    "Protein🥩",
    "Skin care💆",
    "Exercise 🏋️",
    "Family/Friends 👨‍👩‍👧"
    ]

    # --- Inputs for today ---
    st.write("Check everything you did today:")
    checks = {t: st.checkbox(t, key=f"task_{t}") for t in tasks}
    prayers = st.number_input("How many times did you pray today?", 0, 50, 0, key="prayers")
    date_today = st.date_input("Date", dt.date.today(), key="date_today")


    # --- Scores ---
    score_daily = sum(checks.values()) * POINTS_PER_TASK + prayers * PRAYER_BONUS
    st.write("### Daily productivity score:", score_daily)

    # Mood
    if score_daily <= 100: mood = "Awful 😞"
    elif score_daily <= 200: mood = "Bad 😔"
    elif score_daily <= 300: mood = "Normal 😐"
    elif score_daily <= 400: mood = "Good 🙂"
    else: mood = "Great 😄"
    st.subheader(f"**Mood:** {mood}")
#create  daily data
    Days= [200,325]
    df = pd.DataFrame({"Day": Days})
    st.dataframe(df)
#travel Tab
    with tab_travel:
        st.title("Travel checklist")
        st.write("Check everything you have packed")
        tasks = [
            "Passport/ID", "Charger", "Cell phones", "Laptop", "Meds", "Clothes", "Toiletries", "ATM cards"
        ]
        checks = {t: st.checkbox(t) for t in tasks}

        st.write("Travel safe")



