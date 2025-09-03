import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Class Schedule", layout="wide")

# -------------------------
# Custom CSS for styling
# -------------------------
st.markdown(
    """
    <style>
        /* Animated gradient background */
        .stApp {
            background: linear-gradient(-45deg, #a18cd1, #fbc2eb, #8ec5fc, #e0c3fc);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Title Box */
        .title-box {
            background-color: #2c3e50; /* dark grey */
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }
        .title-box h1 {
            color: #5dade2;
            margin: 0;
        }
        .title-box h3 {
            color: #5dade2;
            margin: 0;
            font-weight: normal;
        }

        /* Class Box */
        .class-box {
            background-color: #34495e; /* dark grey */
            padding: 12px;
            border-radius: 12px;
            margin: 8px 0;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.25);
            color: white;
        }

        /* Breaks */
        .break-box {
            background-color: #d5f5e3;
            padding: 10px;
            border-radius: 10px;
            margin: 8px 0;
            text-align: center;
            font-style: italic;
            font-weight: bold;
            color: #27ae60;
        }

        /* Notices Box */
        .notices-box {
            background-color: #fef9e7;
            padding: 15px;
            border-radius: 12px;
            margin-top: 20px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
            color: #2c3e50; /* Make all text inside dark */
        }
        
        /* Assignments Box */
        .assignments-box {
            background-color: #eaf2f8; /* light blue */
            padding: 15px;
            border-radius: 12px;
            margin-top: 20px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
            color: #2c3e50; /* Make all text inside dark */
        }

        /* Status Box for Now/Next */
        .status-container {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 5px 20px 20px 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            text-align: center;
        }
        .status-box {
            background-color: #34495e;
            padding: 12px;
            border-radius: 12px;
            margin: 10px 0;
            color: white;
            font-weight: bold;
        }

        /* Tabs */
        .stTabs [role="tab"] {
            font-weight: bold;
            color: white !important;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            color: #5dade2 !important;
        }

        /* Footer */
        footer {
            text-align: center;
            font-size: 1.25em; /* 25% larger */
            margin-top: 40px;
            color: #2c3e50;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Load Data
# -------------------------
def load_schedule(file):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        st.error(f"Error: The file '{file}' was not found. Please make sure it's in the same directory.")
        return pd.DataFrame() # Return empty dataframe on error

scheduleA = load_schedule("scheduleA.csv")
scheduleB = load_schedule("scheduleB.csv")

# -------------------------
# Section Selector
# -------------------------
section = st.radio(
    "Select Section",
    ["BSCE-1A", "BSCE-1B"],
    horizontal=True,
    key="section_selector"
)

schedule = scheduleA if section == "BSCE-1A" else scheduleB

# -------------------------
# Title Box
# -------------------------
st.markdown(
    f"""
    <div class="title-box">
        <h1>{section}</h1>
        <h3>Schedule Made Easy</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Happening Now & Next Up Box
# -----------------------------------
st.markdown('<div class="status-container">', unsafe_allow_html=True)

# Define the timezone for GMT+5
tz = pytz.timezone('Asia/Karachi')

# Get current time in the specified timezone
now = datetime.now(tz)
current_time_obj = now.time()
today = now.strftime("%A")

today_schedule = schedule[schedule["Day"] == today].copy()

current_class = None
next_class = None

if not today_schedule.empty:
    # Convert time strings to datetime.time objects for correct comparison
    today_schedule['start_time_obj'] = pd.to_datetime(today_schedule['Start_Time'], format='%H:%M').dt.time
    today_schedule['end_time_obj'] = pd.to_datetime(today_schedule['End_Time'], format='%H:%M').dt.time

    # Sort schedule chronologically
    today_schedule = today_schedule.sort_values(by="start_time_obj")

    for _, row in today_schedule.iterrows():
        # Check for the currently happening class
        if row['start_time_obj'] <= current_time_obj <= row['end_time_obj']:
            current_class = row
        # Find the *first* class that is after the current time
        elif row['start_time_obj'] > current_time_obj and next_class is None:
            next_class = row

if current_class is not None:
    st.markdown(
        f"""
        <div class="status-box">
            📘 Happening Now: <br>
            {current_class['Course']} <br>
            ⏰ {current_class['Start_Time']} - {current_class['End_Time']} <br>
            👨‍🏫 {current_class['Teacher']} <br>
            📍 {current_class['Venue']}
        </div>
        """,
        unsafe_allow_html=True
    )

if next_class is not None:
    st.markdown(
        f"""
        <div class="status-box">
            ⏭️ Next Up: <br>
            {next_class['Course']} <br>
            ⏰ {next_class['Start_Time']} - {next_class['End_Time']} <br>
            👨‍🏫 {next_class['Teacher']} <br>
            📍 {next_class['Venue']}
        </div>
        """,
        unsafe_allow_html=True
    )

# Handle cases where there are no classes today or classes are over
if today_schedule.empty:
    st.info(f"🎉 No classes scheduled for today ({today})!")
elif current_class is None and next_class is None:
    st.info("🎉 All classes for today are over!")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Tabs for Days
# -------------------------
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
days = sorted(schedule["Day"].unique(), key=lambda day: day_order.index(day) if day in day_order else -1)

if not days:
    st.warning("The selected schedule file is empty or invalid.")
else:
    tabs = st.tabs(days)
    # -------------------------
    # Show schedule per day
    # -------------------------
    for i, day in enumerate(days):
        with tabs[i]:
            day_schedule = schedule[schedule["Day"] == day].copy()
            
            day_schedule['Start_Time_dt'] = pd.to_datetime(day_schedule['Start_Time'], format='%H:%M')
            day_schedule = day_schedule.sort_values(by="Start_Time_dt")

            prev_end = None
            for _, row in day_schedule.iterrows():
                start = datetime.strptime(row["Start_Time"], "%H:%M")
                end = datetime.strptime(row["End_Time"], "%H:%M")

                if prev_end:
                    gap_minutes = (start - prev_end).total_seconds() / 60
                    if gap_minutes > 15: # Only display breaks longer than 15 mins
                        
                        # Calculate hours and minutes for display
                        hours = int(gap_minutes // 60)
                        minutes = int(gap_minutes % 60)
                        
                        display_text = ""
                        if hours > 0:
                            display_text += f"{hours} hr "
                        if minutes > 0:
                            display_text += f"{minutes} min"
                        
                        st.markdown(f'<div class="break-box">☕ Break ({display_text.strip()})</div>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="class-box">
                        <b>📘 {row['Course']}</b><br>
                        ⏰ {row['Start_Time']} - {row['End_Time']}<br>
                        👨‍🏫 {row['Teacher']}<br>
                        📍 {row['Venue']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                prev_end = end

# ------------------------------------------------------------------
# DYNAMIC Notices and Assignments Sections
# ------------------------------------------------------------------
# Check which section is selected and display content accordingly
if section == "BSCE-1A":
    # --- Notices for section 1A ---
    st.markdown(
        """
        <div class="notices-box">
            <h3>📢 Notices for BSCE-1A</h3>
            <ul>
                <li>Report any bugs/issues or change of schedule to me on Whatsapp </li>
                <li> </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    # --- Assignments for section 1A ---
    st.markdown(
        """
        <div class="assignments-box">
            <h3>📝 Assignments Due for BSCE-1A</h3>
            <ul>
                <li><b></li>
                <li><b></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

elif section == "BSCE-1B":
    # --- Notices for section 1B ---
    st.markdown(
        """
        <div class="notices-box">
            <h3>📢 Notices for BSCE-1B</h3>
            <ul>
                <li>Report any bugs or issues to me on whatsapp </li>
                <li> Calculus Quiz will be scheduled after completion of Ex 3 as per Book </li>
                <li> AP Quiz will scheduled in the 5th week <li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    # --- Assignments for section 1B ---
    st.markdown(
        """
        <div class="assignments-box">
            <h3>📝 Assignments Due for BSCE-1B</h3>
            <ul>
                <li><b>Physics Lab:Complete Lab 1 all tasks (Submission on Thursday) </b> </li>
                <li><b>ICT:write a brief two-page assignment on the history of computers (500_600 words). [Submission on Saturday through GCR{  </b></li>
                <li><b> Applied Physics: Complete all examples for vectors and forces given in slides </b></li>
                <li><b> Eng: Complete Excercise 7-15 in the manual </b></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------
# Footer
# -------------------------
st.markdown("<footer>Created by Wassay Ahmed</footer>", unsafe_allow_html=True)






