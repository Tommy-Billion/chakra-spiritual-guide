import streamlit as st
from openai import OpenAI

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Chakra — Spiritual Guidance",
    page_icon="✨",
    layout="centered"
)

# ===== STYLING (GLOBAL PREMIUM) =====
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #0e1117;
    color: #ffffff;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #a0a0a0;
    margin-bottom: 40px;
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

# ===== TITLE =====
st.markdown('<div class="main-title">Chakra</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Global Spiritual Guidance</div>', unsafe_allow_html=True)

# ===== INPUT =====
user_input = st.text_input("Ask for spiritual guidance")

# ===== OPENAI CLIENT =====
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ===== RESPONSE =====
if st.button("Receive Guidance") and user_input:
    with st.spinner("Connecting to spiritual insight..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are Chakra, a calm, wise, globally inclusive spiritual guide. Speak with clarity, warmth, and depth. Avoid religion-specific language unless asked."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.8
        )

        answer = response.choices[0].message.content

        st.markdown(
            f'<div class="response-box">{answer}</div>',
            unsafe_allow_html=True
        )

# ===== FOOTER =====
st.markdown(
    "<div style='text-align:center; margin-top:40px; color:#666;'>© Chakra Spiritual Guidance</div>",
    unsafe_allow_html=True
)
