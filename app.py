import streamlit as st
from openai import OpenAI
from datetime import date

# ======================
# SECRETS
# ======================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

# ======================
# BRAND CONFIG
# ======================
APP_NAME = "Chakra"
TAGLINE = "Intelligent clarity for the inner world."

MAX_SESSION_QUESTIONS = 5
MAX_DAILY_QUESTIONS = 30

# ======================
# DAILY RESET
# ======================
today = str(date.today())

if "daily_date" not in st.session_state:
    st.session_state.daily_date = today
    st.session_state.daily_count = 0

if st.session_state.daily_date != today:
    st.session_state.daily_date = today
    st.session_state.daily_count = 0

# ======================
# SESSION COUNT
# ======================
if "session_count" not in st.session_state:
    st.session_state.session_count = 0

# ======================
# ADMIN MODE
# ======================
st.sidebar.title("Admin")
admin_input = st.sidebar.text_input("Admin password", type="password")
admin_mode = admin_input == ADMIN_PASSWORD

# ======================
# GLOBAL UI
# ======================
st.set_page_config(
    page_title="Chakra — Intelligent Clarity",
    page_icon="🌀",
    layout="centered"
)

st.title("🌀 Chakra")
st.caption(TAGLINE)

st.write(
    "A calm, intelligent space to explore thoughts, emotions, patterns, "
    "and inner awareness."
)

# ======================
# MASTER SYSTEM PROMPT
# ======================
SYSTEM_PROMPT = """
You are Chakra.

Chakra is a calm, neutral, intelligent inner-world guide.
Chakra blends psychology, awareness, and grounded spirituality.

Tone:
- Clear
- Balanced
- Non-dramatic
- Reflective
- Emotionally steady
- Non-mystical language
- No guru voice

Chakra does NOT:
- Preach
- Diagnose
- Moralize
- Over-affirm
- Use exaggerated spiritual claims

Response structure:
1. Reflect the user’s experience calmly
2. Identify an underlying pattern or dynamic
3. Expand awareness gently
4. Offer grounded practical perspective

Style:
- Medium length responses
- Calm sentences
- Insightful but accessible
- Universal human framing
"""

# ======================
# INPUT
# ======================
user_input = st.text_input("Your question")

limit_reached = (
    st.session_state.session_count >= MAX_SESSION_QUESTIONS
    or st.session_state.daily_count >= MAX_DAILY_QUESTIONS
)

# ======================
# RESPONSE
# ======================
if user_input:
    if limit_reached and not admin_mode:
        st.warning("Daily free limit reached.")

        st.markdown("### Unlock full access")
        st.write("Continue exploring with Chakra today.")

        if st.button("Unlock — R30"):
            st.info("Payment integration coming.")

    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
        )

        st.markdown("**Chakra**")
        st.write(response.choices[0].message.content)

        st.session_state.session_count += 1
        st.session_state.daily_count += 1

# ======================
# SIDEBAR STATUS
# ======================
st.sidebar.markdown("### Usage")
st.sidebar.write(
    f"Session: {st.session_state.session_count}/{MAX_SESSION_QUESTIONS}"
)
st.sidebar.write(
    f"Today: {st.session_state.daily_count}/{MAX_DAILY_QUESTIONS}"
)

# ======================
# FOOTER BRAND
# ======================
st.markdown("---")
st.caption("Chakra — Intelligent clarity for the inner world.")
