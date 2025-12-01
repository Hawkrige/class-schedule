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

        /* GPA Calculator specific */
        .gpa-box {
            background-color: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
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
    ["BSCE-1A", "BSCE-1B", "GPA Calc"],
    horizontal=True,
    key="section_selector"
)

# -------------------------
# GPA CALCULATOR LOGIC
# -------------------------
if section == "GPA Calc":
    st.markdown(
        f"""
        <div class="title-box">
            <h1>GPA Calculator</h1>
            <h3>Projected Grades based on Performance</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("ℹ️ **Instructions:** Enter your obtained marks in the format **Obtained/Total** (e.g., `8/10`). Leave fields blank if the assessment hasn't happened yet; the system will project your score based on entered marks.")

    # Helper function to parse "x/y" string
    def get_score_percentage(entry):
        if not entry:
            return None
        try:
            if "/" in entry:
                obtained, total = map(float, entry.split('/'))
                return obtained / total
            else:
                # Fallback if user just types a number (assume out of 10 or 100? Safest to ignore or treat as raw)
                # To stick to instructions, we expect x/x
                return None
        except ValueError:
            return None

    # Helper to convert percentage to Grade Point (Standard 4.0 scale assumption)
    def pct_to_gp(pct):
        if pct >= 85: return 4.0
        elif pct >= 80: return 3.67
        elif pct >= 75: return 3.33
        elif pct >= 70: return 3.0
        elif pct >= 67: return 2.67
        elif pct >= 64: return 2.33
        elif pct >= 60: return 2.0
        elif pct >= 57: return 1.67
        elif pct >= 54: return 1.33
        elif pct >= 50: return 1.0
        else: return 0.0

    # Data Structure for Subjects and Weights
    subjects_data = [
        {
            "name": "OHS", "cr": 1,
            "components": [
                ("Quiz 1", 10), ("Quiz 2", 10), ("Assignment 1", 5), ("Assignment 2", 5),
                ("Report 1", 5), ("Report 2", 5), ("Mid 1", 15), ("Mid 2", 15), ("Finals", 40)
            ]
        },
        {
            "name": "Islamiat", "cr": 2,
            "components": [
                ("Quiz 1", 3.34), ("Quiz 2", 3.33), ("Quiz 3", 3.33), ("Quiz/Viva", 5),
                ("Class Participation", 5), ("Mid 1", 15), ("Mid 2", 15), ("Finals", 50)
            ]
        },
        {
            "name": "ICP", "cr": 2,
            "components": [
                ("Quiz 1", 5), ("Quiz 2", 5), ("Quiz 3", 5), ("Quiz 4", 5),
                ("Mid 1", 15), ("Mid 2", 15), ("Finals", 50)
            ]
        },
        {
            "name": "Applied Physics", "cr": 2,
            "components": [
                ("Quiz 1", 2), ("Quiz 2", 2), ("Quiz 3", 2),
                ("Assignment 1", 3), ("Assignment 2", 3), ("Assignment 3", 3),
                ("Attendance", 5), ("Mid 1", 15), ("Mid 2", 15), ("Final", 50)
            ]
        },
        {
            "name": "Applied Calculus", "cr": 3,
            "components": [
                ("Quiz 1", 2), ("Quiz 2", 2), ("Quiz 3", 2), ("Quiz 4", 2),
                ("Assignment 1", 3), ("Assignment 2", 3), ("Assignment 3", 3),
                ("Mid 1", 15), ("Mid 2", 15), ("Final", 50)
            ]
        },
        {
            "name": "English", "cr": 3,
            "components": [
                ("Assignment 1", 2), ("Assignment 2", 1), ("Assignment 3", 2),
                ("Quiz 1", 2), ("Quiz 2", 1), ("Quiz 3", 2),
                ("Mid 1", 15), ("Mid 2", 15), ("Project", 4), ("Presentation", 6), ("Final", 50)
            ]
        },
        {
            "name": "ICT", "cr": 2,
            "components": [
                ("Assignment 1", 5), ("Assignment 2", 5), ("Quiz 1", 5), ("Quiz 2", 5),
                ("Mid 1", 15), ("Mid 2", 15), ("Final", 50)
            ]
        },
        {
            "name": "AP Lab", "cr": 1,
            "components": [
                ("Quiz 1", 7), ("Quiz 2", 8), ("Lab work", 52), ("Project", 3), ("Final", 30)
            ]
        },
        {
            "name": "ICT Lab", "cr": 1,
            "components": [
                ("Lab work", 36), ("Quiz", 6), ("Project", 4), ("Final", 50)
            ]
        }
    ]

    total_credits = 0
    total_weighted_points = 0
    
    st.markdown('<div class="gpa-box">', unsafe_allow_html=True)
    
    # Generate Inputs
    with st.form("gpa_form"):
        col_idx = 0
        cols = st.columns(3) # 3 subjects per row layout

        results_data = []

        for sub in subjects_data:
            with cols[col_idx % 3]:
                with st.expander(f"**{sub['name']}** ({sub['cr']} Cr)"):
                    weighted_sum_obtained = 0
                    total_weight_attempted = 0
                    
                    sub_inputs = {}
                    for comp_name, comp_weight in sub['components']:
                        val = st.text_input(f"{comp_name} ({comp_weight}%)", key=f"{sub['name']}_{comp_name}", placeholder="e.g. 8/10")
                        
                        ratio = get_score_percentage(val)
                        if ratio is not None:
                            weighted_sum_obtained += (ratio * comp_weight)
                            total_weight_attempted += comp_weight
                    
                    results_data.append({
                        "subject": sub,
                        "obtained_weight": weighted_sum_obtained,
                        "attempted_weight": total_weight_attempted
                    })
            col_idx += 1
        
        submitted = st.form_submit_button("Calculate GPA")

    if submitted:
        st.markdown("---")
        st.subheader("Results")
        
        # Calculation Logic
        valid_calculation = True
        
        for data in results_data:
            sub = data['subject']
            obt_w = data['obtained_weight']
            att_w = data['attempted_weight']
            
            # Projection Logic
            if att_w == 0:
                # No marks entered for this subject
                final_percentage = 0.0
                gpa = 0.0
                st.warning(f"⚠️ **{sub['name']}**: No marks entered. Treated as 0.0 GPA.")
            else:
                # Project performance to 100%
                # Logic: (Obtained Weight / Attempted Weight) * 100
                final_percentage = (obt_w / att_w) * 100
                gpa = pct_to_gp(final_percentage)
                
                st.write(f"**{sub['name']}**: Projected Score: `{final_percentage:.2f}%` | GPA: `{gpa}`")

            total_credits += sub['cr']
            total_weighted_points += (sub['cr'] * gpa)

        if total_credits > 0:
            final_gpa = total_weighted_points / total_credits
            st.markdown(
                f"""
                <div style="background-color: #2c3e50; padding: 20px; border-radius: 10px; text-align: center; color: #5dade2; margin-top: 20px;">
                    <h2>Calculated CGPA: {final_gpa:.2f}</h2>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.error("No credits found to calculate.")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# SCHEDULE LOGIC (Run only if section is NOT GPA Calc)
# -------------------------
else:
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
                    <li><b>All classes scheduled for 8th and 9th Sept will be conducted online due to adverse weather</b></li>
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
                    <li><b> </b> </li>
                    <li><b></b></li>
                    
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
                    <li>  </li>
                    <li>    </li>
                    <li> <b></b> </li>
                    
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
                    <li><b>ICT Lab:Complete Lab 5 : Intro to Viso and Flutter flow (Submission on Monday) </b> </li>
                    <li><b>  </b></li>
                    <li><b>  </b></li>
                    <li><b> Eng:  </b></li>
                    <li><b> </b><li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------
# Footer
# -------------------------
st.markdown("<footer>Created by Wassay Ahmed</footer>", unsafe_allow_html=True)







