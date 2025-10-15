import streamlit as st
import pandas as pd
import datetime as dt
import os

st.set_page_config(page_title="Daily Mood Tracker", page_icon="😄", layout="centered")
st.title("🌤️ Daily Productivity & Mood Tracker")

# --- Config ---
CSV_PATH = "daily_log.csv"
POINTS_PER_TASK = 25
PRAYER_BONUS = 25
tasks = [
    "Eat x2","Code","Hot tub","Swimming","Ice cream","Game","TV",
    "Read","Write","Drive","Park","Clean","Cook","Protein","Skin care",
    "Exercise","Family/Friends"
]

# --- Inputs for today ---
st.write("Check everything you did today:")
checks = {t: st.checkbox(t) for t in tasks}
prayers = st.number_input("How many times did you pray today?", 0, 50, 0)
date_today = st.date_input("Date", dt.date.today())

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

# --- Save today ---
def row_for_csv():
    return {
        "date": date_today.isoformat(),
        **{f"done_{k}": int(v) for k, v in checks.items()},
        "prayers": int(prayers),
        "score_daily": int(score_daily),
        "mood": mood
    }

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Save today"):
        new_row = pd.DataFrame([row_for_csv()])
        if os.path.exists(CSV_PATH):
            old = pd.read_csv(CSV_PATH)
            df = pd.concat([old, new_row], ignore_index=True)
            # keep last entry per date
            df = df.drop_duplicates(subset=["date"], keep="last")
        else:
            df = new_row
        df.to_csv(CSV_PATH, index=False)
        st.success("Saved ✅")

with col2:
    if st.button("🧹 Clear history (local)"):
        if os.path.exists(CSV_PATH):
            os.remove(CSV_PATH)
            st.warning("History cleared.")
        else:
            st.info("No file to clear.")

# --- Show history ---
if os.path.exists(CSV_PATH):
    hist = pd.read_csv(CSV_PATH)
    # Ensure date sorted
    hist["date"] = pd.to_datetime(hist["date"])
    hist = hist.sort_values("date")
    st.write("### 📒 History")
    st.dataframe(hist, use_container_width=True)

    # Weekly summary (last 7 days if available)
    last7 = hist.tail(7)
    if not last7.empty:
        weekly_total = int(last7["score_daily"].sum())
        weekly_pct = weekly_total / (len(last7) * (len(tasks)*POINTS_PER_TASK + 50*PRAYER_BONUS/2)) * 100
        st.write(f"**Last 7 days total:** {weekly_total}")
        st.write(f"**Approx. weekly productivity:** {weekly_pct:.1f}%")

    # Chart
    st.write("### 📈 Trend")
    chart_df = hist[["date","score_daily"]].set_index("date")
    st.line_chart(chart_df)
else:
    st.info("No history yet. Save today to start your log.")


