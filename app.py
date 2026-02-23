import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai
from datetime import datetime
import requests

# הגדרות דף
st.set_page_config(page_title="OSINT STRATEGIC TRACKER", layout="wide")

# ניסיון חיבור ל-API של Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = None

# פונקציות לשאיבת נתונים (Placeholder לנתונים חיים)
def get_live_data():
    # כאן בעתיד נחבר APIs אמיתיים
    return {
        "oil": "72.45",
        "rial": "615,000",
        "gps": "Severe Interference (Northern Israel)",
        "polymarket": "64%"
    }

data = get_live_data()

# עיצוב בסגנון חמ"ל (Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stButton>button { width: 100%; background-color: #1a1a1a; color: #00FF41; border: 1px solid #00FF41; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ OSINT STRATEGIC TRACKER")
st.write(f"🛡️ **System Status:** Online | **Last Scan:** {datetime.now().strftime('%H:%M:%S')}")

# שורת מדדים
c1, c2, c3, c4 = st.columns(4)
c1.metric("Brent Oil", f"${data['oil']}")
c2.metric("IRR/USD (Black Market)", data['rial'])
c3.metric("War Probability", data['polymarket'])
c4.metric("GPS Status", "JAMMING", delta="Active", delta_color="inverse")

st.divider()

# לוגיקת ה-AI
st.header("🤖 Gemini Strategic Analysis")
if model:
    if st.button("Generate Tactical Insight"):
        prompt = f"""נתח את המצב הבא: מחיר הנפט {data['oil']}, שער הריאל {data['rial']}, ושיבושי GPS פעילים. 
        מה האינדיקציה המודיעינית המיידית? ענה בעברית תמציתית בסגנון דוח אמ"ן."""
        response = model.generate_content(prompt)
        st.info(response.text)
else:
    st.warning("⚠️ המתן לחיבור API Key ב-Streamlit Secrets")

# טבלת יומן אירועים
st.subheader("📋 Operations Log")
logs = pd.DataFrame([
    {"Time": "22:15", "Event": "U.S. Tanker tracking Kharg Island move", "Level": "HIGH"},
    {"Time": "21:40", "Event": "Flight cancellations: Tehran Intl Airport", "Level": "CRITICAL"},
    {"Time": "20:10", "Event": "GPS Spoofing detected over Haifa Bay", "Level": "MEDIUM"}
])
st.table(logs)
