import streamlit as st
from openai import OpenAI
from datetime import date
import streamlit.components.v1 as components

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Chakra",
    page_icon="assets/chakra_icon.png",
    layout="centered"
)

# =========================
# CENTERED LOTUS ICON + TITLE
# =========================
st.image("assets/chakra_icon.png", width=130)
st.markdown(
    '<div style="text-align:center; font-size:42px; font-weight:600; margin-top:10px;">Chakra</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div style="text-align:center; font-size:18px; color:#a0a0a0; margin-bottom:30px;">Global Spiritual Guidance</div>',
    unsafe_allow_html=True
)

# =========================
# CHAKRA CUSTOM MENU (tap-friendly)
# =========================
menu_html = """
<style>
.chakra-menu-container {
    position: fixed;
    top: 18px;
    right: 20px;
    z-index: 9999;
    font-family: 'Segoe UI', sans-serif;
}

.chakra-menu-button {
    font-size: 26px;
    cursor: pointer;
    color: white;
}

.chakra-menu-content {
    display: none;
    position: absolute;
    right: 0;
    background-color: #1c1f26;
    min-width: 200px;
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    overflow: hidden;
}

.chakra-menu-content a {
    color: white;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.chakra-menu-content a:hover {
    background-color: #2a2f3a;
}
</style>

<div class="chakra-menu-container">
  <div class="chakra-menu-button" onclick="var menu=this.nextElementSibling; menu.style.display=(menu.style.display=='block')?'none':'block';">☰</div>
  <div class="chakra-menu-content">
    <a href="#" onclick="navigator.clipboard.writeText(window.location.href);alert('Chakra link copied ✨');">Share Chakra Energy</a>
    <a href="#" onclick="alert('To add Chakra: open browser menu → Add to Home Screen');">Add to Home</a>
    <a href="#" onclick="window.close();">Exit</a>
  </div>
</div>
"""

components.html(menu_html, height=0)

# =========================
# GLOBAL STYLING
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #0e1117;
    color: #ffffff;
}

.stTextInput > div > div > input {
    background-color: #1c1f26;
    color: white;
    border-radius: 12px;
    padding: 12px;
}

.stButton button {
    width: 100%;
    border-radius: 12px;
    padding: 12px;
    background: linear-gradient(90deg, #7b5cff, #00c2ff);
    color: white;
    font-weight: 600;
    border: none;
}

.response-box {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 14px;
    margin-top: 25px;
    line-height: 1.6;
    font-size: 17px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD SECRETS
# =========================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

MAX_SESSION_QUESTIONS = 5
MAX_DAILY_QUESTIONS = 30

# =========================
# DAILY RESET
# =========================
today = str(date.today())

if "daily_date" not in st.session_state:
    st.session_state.daily_date = today
    st.session_state.daily_count = 0

if st.session_state.daily_date != today:
    st.session_state.daily_date = today
    st.session_state.daily_count = 0

# =========================
# SESSION COUNT
# =========================
if "session_count" not in st.session_state:
    st.session_state.session_count = 0

# =========================
# ADMIN SIDEBAR
# =========================
st.sidebar.title("Admin")
admin_input = st.sidebar.text_input("Admin password", type="password")
admin_mode = admin_input == ADMIN_PASSWORD

# =========================
# USER INPUT
# =========================
user_input = st.text_input("Ask for spiritual guidance")

limit_reached = (
    st.session_state.session_count >= MAX_SESSION_QUESTIONS
    or st.session_state.daily_count >= MAX_DAILY_QUESTIONS
)

# =========================
# RESPONSE LOGIC
# =========================
if st.button("Receive Guidance") and user_input:

    if limit_reached and not admin_mode:
        st.warning("Daily free guidance limit reached 🌿")
        st.markdown("### 🔓 Unlimited Chakra Access")
        st.write("Premium access unlocking soon.")

        if st.button("Unlock — R30"):
            st.info("Payment integration coming soon 🌍")

    else:
        with st.spinner("Connecting to spiritual insight..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are Chakra, a calm, wise, globally inclusive spiritual guide.

Your communication style:
- Grounded
- Emotionally intelligent
- Non-religious unless asked
- Clear and reflective
- Supportive but not preachy
- Universal language
- Gentle insight

You help users explore:
thoughts, emotions, inner patterns, meaning, awareness, presence, growth.

Avoid mystical exaggeration.
Avoid spiritual superiority.
Speak like a wise human mentor.
"""
                    },
                    {"role": "user", "content": user_input}
                ],
                temperature=0.8
            )

            answer = response.choices[0].message.content

            st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)
            st.session_state.session_count += 1
            st.session_state.daily_count += 1

# =========================
# FOOTER
# =========================
st.markdown(
    "<div style='text-align:center; margin-top:40px; color:#666;'>© Chakra Spiritual Guidance</div>",
    unsafe_allow_html=True
)

# =========================
# SIDEBAR USAGE
# =========================
st.sidebar.markdown("### Usage")
st.sidebar.write("Session:", st.session_state.session_count, "/", MAX_SESSION_QUESTIONS)
st.sidebar.write("Today:", st.session_state.daily_count, "/", MAX_DAILY_QUESTIONS)
