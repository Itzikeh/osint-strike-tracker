import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# הגדרות עיצוב מתקדמות למראה "חמ"ל"
st.set_page_config(page_title="STRATEGIC INTEL HUB", layout="wide")

# CSS מותאם אישית למראה Cyber-Audit מרשים
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'JetBrains Mono', monospace;
        background-color: #050505;
        color: #00ff41;
    }
    
    .stApp {
        background: radial-gradient(circle at center, #0a1a0a 0%, #050505 100%);
    }

    /* כרטיסיות אינדיקטורים */
    .metric-card {
        background: rgba(15, 15, 15, 0.8);
        border: 1px solid #1f1f1f;
        padding: 15px;
        border-radius: 4px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
    }
    
    .status-critical { color: #ff003c; text-shadow: 0 0 5px #ff003c; }
    .status-warning { color: #ffaa00; }
    .status-normal { color: #00ff41; }
    
    .header-box {
        border-left: 5px solid #00ff41;
        padding-left: 15px;
        margin-bottom: 25px;
    }
    
    /* עיצוב ה-AI */
    .ai-response {
        background: rgba(255, 255, 255, 0.03);
        border-right: 3px solid #ff003c;
        padding: 20px;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# חיבור ל-AI - פתרון שגיאת 404
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # ניסיון טעינה של מספר וריאציות כדי למנוע קריסה
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
        model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# כותרת האפליקציה
st.markdown("<div class='header-box'><h1>STRATEGIC OSINT TRACKER v2.0</h1><p>REAL-TIME REGIONAL THREAT MONITOR</p></div>", unsafe_allow_html=True)

# פונקציה ליצירת כרטיס מעוצב
def draw_indicator(label, value, status="normal"):
    status_class = f"status-{status}"
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.7rem; color: #888;">{label}</div>
            <div class="{status_class}" style="font-size: 1.2rem; font-weight: bold;">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- חלוקה ל-5 קטגוריות (24 אינדיקטורים) ---

with st.container():
    st.subheader("🌐 MARKET & MARITIME")
    col = st.columns(5)
    with col[0]: draw_indicator("War Risk Premium", "CRITICAL", "critical")
    with col[1]: draw_indicator("Brent Oil Anomaly", "$65.20", "warning")
    with col[2]: draw_indicator("Polymarket Probability", "78%", "critical")
    with col[3]: draw_indicator("IRR Black Market", "618K", "warning")
    with col[4]: draw_indicator("Kharg Terminal AIS", "ZERO", "critical")

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    st.subheader("✈️ AVIATION OSINT")
    col = st.columns(4)
    with col[0]: draw_indicator("ISR Civilian Fleet", "EVACUATED", "warning")
    with col[1]: draw_indicator("ESCAT Saudi", "ACTIVE", "critical")
    with col[2]: draw_indicator("Iran Flight Status", "SUSPENDED", "critical")
    with col[3]: draw_indicator("VIP Flight Track", "DEPARTING", "warning")

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    st.subheader("⚔️ MILITARY POSTURE")
    col = st.columns(5)
    with col[0]: draw_indicator("USS Georgia", "DETECTED", "critical")
    with col[1]: draw_indicator("KC-46 Refueling", "SPIKE", "warning")
    with col[2]: draw_indicator("B-2 Deployment", "ACTIVE", "critical")
    with col[3]: draw_indicator("Nuclear Facilities", "SEALING", "critical")
    with col[4]: draw_indicator("IRGC Leadership", "BUNKERED", "critical")

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    st.subheader("📡 CYBER & SIGINT")
    col = st.columns(6)
    with col[0]: draw_indicator("Gulf Social", "PANIC", "warning")
    with col[1]: draw_indicator("Net Blackouts", "ACTIVE", "critical")
    with col[2]: draw_indicator("GPS Jamming", "LEVEL 5", "critical")
    with col[3]: draw_indicator("Proxy Chatter", "SILENT", "warning")
    with col[4]: draw_indicator("SIGINT Spikes", "HIGH", "critical")
    with col[5]: draw_indicator("Infra-Cyber", "SCANS", "warning")

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    st.subheader("🌍 DIPLOMACY & DEFENSE")
    col = st.columns(4)
    with col[0]: draw_indicator("Summit Deception", "ACTIVE", "warning")
    with col[1]: draw_indicator("Witkoff Plane", "EXITED", "critical")
    with col[2]: draw_indicator("Embassy Status", "EVACUATING", "critical")
    with col[3]: draw_indicator("Hospital Readiness", "CODE RED", "critical")

st.divider()

# --- לוג ניתוח AI בסגנון "Terminal" ---
st.subheader("⚡ AI COMMANDER ANALYSIS")
if st.button("EXECUTE DATA SYNTHESIS"):
    if model:
        try:
            prompt = "Analyze these 24 indicators for imminent war. Priority: Critical. Format: Military Intel Report. Language: Hebrew."
            response = model.generate_content(prompt)
            st.markdown(f"<div class='ai-response'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"SYSTEM FAILURE: {str(e)}")
    else:
        st.error("AI AUTHENTICATION FAILED. CHECK SECRETS.")

# רשימת לוגים כמו באתר ששלחת
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 RECENT LOGS")
logs = pd.DataFrame([
    {"Timestamp": "22:45", "Event": "GPS Spoofing detected over central Israel", "Source": "SIGINT"},
    {"Timestamp": "22:31", "Event": "Chinese Embassy staff leaving Tehran", "Source": "HUMINT"},
    {"Timestamp": "22:15", "Event": "KC-135 Stratotanker heading to Persian Gulf", "Source": "ADS-B"}
])
st.table(logs)
