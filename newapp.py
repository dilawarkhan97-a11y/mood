import streamlit as st
import pandas as pd
import datetime as dt
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Daily Mood Tracker", page_icon="😄", layout="centered")
st.title("🌤️ Daily Productivity & Mood Tracker (Google Sheets)")

# --- Config ---
POINTS_PER_TASK = 25
PRAYER_BONUS = 25
tasks = [
    "Eat x2","Code","Hot tub","Swimming","Ice cream","Game","TV",
    "Read","Write","Drive","Park","Clean","Cook","Protein","Skin care",
    "Exercise","Family/Friends"
]

# --- Connect to Google Sheets ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open_by_key(st.secrets["SHEET_ID"])
ws = sh.sheet1  # use first worksheet

# Ensure header row exists
HEADER = ["date", *[f"done_{t}" for t in tasks], "prayers", "score_daily", "mood"]
first_cell = ws.acell("A1").value
if not first_cell:
    ws.append_row(HEADER)

# --- Inputs for today ---
st.write("Check everything you did today:")
checks = {t: st.checkbox(t) for t in tasks}
prayers = st.number_input("How many times did you pray today?", 0, 50, 0)
date_today = st.date_input("Date", dt.date.today())

# --- Scores & mood ---
score_daily = sum(checks.values()) * POINTS_PER_TASK + prayers * PRAYER_BONUS
st.write("### Daily productivity score:", score_daily)

if score_daily <= 100: mood = "Awful 😞"
elif score_daily <= 200: mood = "Bad 😔"
elif score_daily <= 300: mood = "Normal 😐"
elif score_daily <= 400: mood = "Good 🙂"
else: mood = "Great 😄"
st.subheader(f"**Mood:** {mood}")

# --- Save today ---
if st.button("💾 Save today to Google Sheets"):
    row = [date_today.isoformat(), *[int(checks[t]) for t in tasks], int(prayers), int(score_daily), mood]
    ws.append_row(row, value_input_option="USER_ENTERED")
    st.success("Saved to Google Sheets ✅")

# --- Load history ---
records = ws.get_all_records()
if records:
    hist = pd.DataFrame(records)
    # Coerce date
    hist["date"] = pd.to_datetime(hist["date"], errors="coerce")
    hist = hist.sort_values("date")
    st.write("### 📒 History")
    st.dataframe(hist, use_container_width=True)

    st.write("### 📈 Trend")
    chart_df = hist[["date", "score_daily"]].copy()
    st.line_chart(chart_df.set_index("date"))
else:
    st.info("No history yet. Save today to start your log.")


