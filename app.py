import streamlit as st
import pandas as pd
from datetime import datetime

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Class Schedule", layout="wide")

# ===============================
# CUSTOM STYLES (Animated Gradient + Dark Theme)
# ===============================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(-45deg, #1e1e2f, #2c2c54, #3a3a80, #24243e);
        background-size: 400% 400%;
        animation: gradient 12s ease infinite;
        color: #ffffff;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .grey-box {
        background-color: #2e2e2e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .info-box {
        background-color: #333333;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .break-box {
        background-color: #2e7d32;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        text-align: center;
        font-weight: bold;
    }
    .long-break-box {
        background-color: #1b5e20;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        text-align: center;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: #aaaaaa;
        font-size: 12px;
        margin-top: 30px;
    }
    .stTabs [role="tab"] {
        background-color: #444 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 8px 12px;
        margin-right: 5px;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #ff9800 !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===============================
# SECTION SELECTION (inside grey box)
# ===============================
st.markdown('<div class="grey-box">', unsafe_allow_html=True)
section = st.radio("Select your section:", ["A", "B"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

if section == "A":
    section_title = "BSCE-1A"
    file_name = "scheduleA.csv"
else:
    section_title = "BSCE-1B"
    file_name = "scheduleB.csv"

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv(file_name)
df.columns = df.columns.str.strip().str.lower()

# ===============================
# TITLE + SUBTITLE BOX
# ===============================
st.markdown(
    f"""
    <div class="grey-box">
        <h1 style="color:white;">{section_title}</h1>
        <p style="color:#cccccc;">Schedule made easy</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# FUNCTIONS
# ===============================
def get_current_class(data):
    now = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%A").lower()
    today_classes = data[data["day"].str.lower() == today]
    for _, row in today_classes.iterrows():
        if row["start_time"] <= now <= row["end_time"]:
            return row
    return None

def get_next_class(data):
    now = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%A").lower()
    today_classes = data[data["day"].str.lower() == today]
    upcoming = today_classes[today_classes["start_time"] > now]
    if not upcoming.empty:
        return upcoming.iloc[0]
    return None

def display_breaks(day_classes):
    """Show breaks between classes"""
    day_classes_sorted = day_classes.sort_values("start_time").reset_index(drop=True)
    for i in range(len(day_classes_sorted) - 1):
        end_current = datetime.strptime(day_classes_sorted.loc[i, "end_time"], "%H:%M")
        start_next = datetime.strptime(day_classes_sorted.loc[i+1, "start_time"], "%H:%M")
        gap_minutes = (start_next - end_current).total_seconds() / 60

        if gap_minutes > 120:
            st.markdown(
                f'<div class="long-break-box">☕☕ Long Break ({int(gap_minutes)} min)</div>',
                unsafe_allow_html=True
            )
        elif gap_minutes > 30:
            st.markdown(
                f'<div class="break-box">☕ Break ({int(gap_minutes)} min)</div>',
                unsafe_allow_html=True
            )

# ===============================
# HAPPENING NOW + NEXT UP SECTION
# ===============================
current_class = get_current_class(df)
next_class = get_next_class(df)

st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.subheader("📌 What's Happening Today")

if current_class is not None:
    st.markdown(
        f"""
        <b>Happening Now:</b> 📘 {current_class['course']} <br>
        👤 {current_class['teacher']} | 📍 {current_class['venue']} <br>
        ⏰ {current_class['start_time']} - {current_class['end_time']}
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("✅ No class is happening right now.", unsafe_allow_html=True)

if next_class is not None:
    st.markdown(
        f"""
        <br><b>Next Up:</b> 📘 {next_class['course']} <br>
        👤 {next_class['teacher']} | 📍 {next_class['venue']} <br>
        ⏰ {next_class['start_time']} - {next_class['end_time']}
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<br>🎉 No upcoming class today.", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# TABS FOR EACH DAY
# ===============================
days = df["day"].unique().tolist()
tabs = st.tabs(days)

for i, day in enumerate(days):
    with tabs[i]:
        st.markdown(f"## {day}")
        day_classes = df[df["day"] == day].sort_values("start_time")

        for j in range(len(day_classes)):
            row = day_classes.iloc[j]
            st.markdown(
                f"""
                <div class="info-box">
                    📘 <b>{row['course']}</b><br>
                    👤 {row['teacher']} | 📍 {row['venue']}<br>
                    ⏰ {row['start_time']} - {row['end_time']}
                </div>
                """,
                unsafe_allow_html=True
            )
            # Display breaks between this class and the next
            if j < len(day_classes) - 1:
                end_current = datetime.strptime(row["end_time"], "%H:%M")
                start_next = datetime.strptime(day_classes.iloc[j+1]["start_time"], "%H:%M")
                gap_minutes = (start_next - end_current).total_seconds() / 60
                if gap_minutes > 120:
                    st.markdown(
                        f'<div class="long-break-box">☕☕ Long Break ({int(gap_minutes)} min)</div>',
                        unsafe_allow_html=True
                    )
                elif gap_minutes > 30:
                    st.markdown(
                        f'<div class="break-box">☕ Break ({int(gap_minutes)} min)</div>',
                        unsafe_allow_html=True
                    )

# ===============================
# NOTICES
# ===============================
st.markdown(
    """
    <div class="grey-box">
        <h2 style="color:white;">📢 Notices</h2>
        <p style="color:#cccccc;">If you spot any bugs or mistakes please let me know asap K256558@nu.edu.pk, bsce-1A class order mismatch issue is known </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# FOOTER
# ===============================
st.markdown('<div class="footer">Created by Wassay Ahmed</div>', unsafe_allow_html=True)








