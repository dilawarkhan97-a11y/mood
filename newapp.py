import streamlit as st
import pandas as pd
import datetime as dt
import io
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="My First App", page_icon="📈", layout="centered")
st.title("📈 My first app")

# ---------- TABS ----------
tab_weekly, tab_daily, tab_travel, tab_decision_maker, tab_predictor = st.tabs(["📅 Weekly Overview",
                                                           "🌤️ Daily Tracker",
                                                           "✈️ Travel",
                                                           "📈Decision Maker",
                                                          "🧩Mood Predictor"])

# ---------- WEEKLY TAB ----------
with tab_weekly:  
  prod_per = [27, 65, 69, 71, 65, 70, 68, 63, 40, 55, 73, 88, 75]
  prod_ave = [130, 300, 310, 321, 292, 317, 307, 282, 182, 250, 332, 396, 339]
  weeks = [f"Week {i + 1}" for i in range(len(prod_per))]

  start_date = datetime(2025, 8, 6)
  Dates = [(start_date + timedelta(weeks=i)).strftime("%b %d, %Y") for i in range(len(prod_ave))]

  df = pd.DataFrame({
    "Week": weeks,
    "Productivity (%)": prod_per,
    "Average Output": prod_ave,
    "Dates": Dates
  })

# Add numeric week index for sorting
  df["WeekNum"] = df["Week"].str.extract("(\d+)").astype(int)
  df = df.sort_values("WeekNum")

# Assign grades based on Productivity (%)
  df["Grade"] = pd.cut(
  df["Productivity (%)"],
      bins=[0, 60, 70, 80, 90, 100],
      labels=["F", "D", "C", "B", "A"],
      right=False
    )

# Show table and chart
  st.dataframe(df[["Week", "Dates", "Productivity (%)", "Average Output", "Grade"]], use_container_width=True)
  st.line_chart(df.set_index("Week")[["Productivity (%)", "Average Output"]])


# ---------- DAILY TAB ----------
with tab_daily:
    st.subheader("Daily Productivity & Mood Tracker")

    # --- Config ---

    POINTS_PER_TASK = 25
    PRAYER_BONUS = 25
    tasks = [
        "Eat x2 ",
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
    if score_daily <= 100:
        mood = "Awful 😞"
    elif score_daily <= 200:
        mood = "Bad 😔"
    elif score_daily <= 300:
        mood = "Normal 😐"
    elif score_daily <= 400:
        mood = "Good 🙂"
    else:
        mood = "Great 😄"
    st.subheader(f"**Mood:** {mood}")
    # create  daily data
    Days = [400,425,200,325,350,350,325]
    weekly_mean= np.mean(Days)
    st.write("Weekly Mean:", weekly_mean)
    df = pd.DataFrame({"Day": Days})
    st.dataframe(df)
    # travel Tab
    with tab_travel:
        st.title("Travel checklist")
        st.write("Check everything you have packed")
        tasks = [
            "Passport/ID", "Charger", "Cell phones", "Laptop", "Meds", "Clothes", "Toiletries", "ATM cards"
        ]
        checks = {t: st.checkbox(t) for t in tasks}

        st.write("Travel safe")

    # Tab decision Maker
with tab_decision_maker:
    st.title("🧠 Decision Energy Model")
    st.write(
        "Quantify how attention, emotions, expectations, memories, and perspective shape your outcome probability.")

    Attention = st.slider("⏱️ Time", 0.0, 1.0, 0.5)
    Emotions = st.slider("💖 Emotions", 0.0, 1.0, 0.5)
    Expectations = st.slider("🎯 Expectations", 0.0, 1.0, 0.5)
    Memories = st.slider("🧩 Memories from past are good  or bad", 0.0, 1.0, 0.5)
    Perspective = st.slider("🌌 Superficial or deep", 0.0, 1.0, 0.5)

    import numpy as np

    weight = Attention + Emotions + Expectations + Memories + Perspective
    bias = -0.5 * weight
    Z = weight + bias
    p = 1 / (1 + np.exp(-Z))

  
    st.write(f"**Probability (p) =** {p:.3f}")


with tab_predictor:
    prod_Ave = [200, 300, 310, 321, 292, 317, 307, 282, 182]

    mood = ["Bad 😞", "Normal 😐", "Good 🙂", "Good 🙂", "Normal 😐", "Good 🙂", "Good 🙂", "Normal 😐", "Bad 😞", "Normal 😐", "Good 🙂","Good 🙂"]

    # Show the raw data
    df = pd.DataFrame({"Mood Weekly": mood})
    st.dataframe(df, use_container_width=True)

    # Prepare states and index map
    states = sorted(set(mood))  # e.g., ['Bad 😞', 'Good 🙂', 'Normal 😐']
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)

    # Count transitions
    P = np.zeros((n, n), dtype=float)
    for i in range(len(mood) - 1):  # for loops execute a block of code a fixed number of times
        cur, nxt = mood[i], mood[i + 1]
        P[idx[cur], idx[nxt]] += 1

    # Normalize rows to probabilities (guard against zero rows)
    row_sums = P.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    P = P / row_sums

    # Display transition matrix with labels
    P_df = pd.DataFrame(P, index=states, columns=states)
    st.write("Transition matrix (rows = current, columns = next):")
    st.dataframe(P_df.style.format("{:.2f}"), use_container_width=True)

    # Predict next mood from the last observed mood
    last_state = mood[-1]
    last_vec = np.zeros(n)
    last_vec[idx[last_state]] = 1.0
    next_probs = last_vec @ P

    probs_series = pd.Series(next_probs, index=states).sort_values(ascending=False)
    predicted = probs_series.idxmax()

    st.write("Next mood probabilities:")
    st.write(probs_series.to_frame("probability"))
    st.success(f"Predicted next mood: {predicted}")

































