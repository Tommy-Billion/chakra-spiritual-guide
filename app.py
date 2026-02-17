import streamlit as st
from openai import OpenAI
from datetime import date

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

client = OpenAI(api_key=OPENAI_API_KEY)

MAX_SESSION_QUESTIONS = 5
MAX_DAILY_QUESTIONS = 30

# -------------------
# DAILY RESET
# -------------------
today = str(date.today())

if "daily_date" not in st.session_state:
    st.session_state.daily_date = today
    st.session_state.daily_count = 0

if st.session_state.daily_date != today:
    st.session_state.daily_date = today
    st.session_state.daily_count = 0

# -------------------
# SESSION COUNT
# -------------------
if "session_count" not in st.session_state:
    st.session_state.session_count = 0

# -------------------
# ADMIN MODE
# -------------------
st.sidebar.title("Admin")

admin_input = st.sidebar.text_input("Admin password", type="password")

admin_mode = admin_input == ADMIN_PASSWORD
# -------------------
# ADMIN DASHBOARD
# -------------------
if admin_mode:
    st.sidebar.markdown("### 🔑 Admin Dashboard")

    st.sidebar.write("Session count:", st.session_state.session_count)
    st.sidebar.write("Daily count:", st.session_state.daily_count)
    st.sidebar.write("Daily max:", MAX_DAILY_QUESTIONS)
    st.sidebar.write("Session max:", MAX_SESSION_QUESTIONS)

    # Reset session for all users
    if st.sidebar.button("Reset Session Count"):
        st.session_state.session_count = 0
        st.success("Session count reset 🌿")

    # Reset daily count
    if st.sidebar.button("Reset Daily Count"):
        st.session_state.daily_count = 0
        st.success("Daily count reset 🌞")

# -------------------
# UI
# -------------------
st.title("🌀 Chakra Spiritual Guide")
st.write("Ask anything about spirituality, chakras, healing, or inner growth.")

system_prompt = """
You are Chakra, a spiritually intelligent AI guide.
You provide calm, wise, supportive spiritual guidance.
"""

user_input = st.text_input("Your question:")

# -------------------
# LIMIT CHECK
# -------------------
limit_reached = (
    st.session_state.session_count >= MAX_SESSION_QUESTIONS
    or st.session_state.daily_count >= MAX_DAILY_QUESTIONS
)

if user_input:
    if limit_reached and not admin_mode:
        st.warning("Chakra has reached today's free energy limit 🌿")

        st.markdown("### 🔓 Unlock Chakra Guidance")
        st.write("Continue receiving spiritual guidance today.")

        if st.button("Unlock – R30"):
            st.info("Payment link coming soon 🌿")

    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )

        st.markdown("**Chakra:**")
        st.write(response.choices[0].message.content)

        st.session_state.session_count += 1
        st.session_state.daily_count += 1

# -------------------
# STATUS
# -------------------
st.sidebar.markdown("### Usage")
st.sidebar.write("Session:", st.session_state.session_count, "/", MAX_SESSION_QUESTIONS)
st.sidebar.write("Today:", st.session_state.daily_count, "/", MAX_DAILY_QUESTIONS)
