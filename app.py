import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import google.generativeai as genai
from datetime import datetime
import time

# הגדרות דף רחבות וכהות
st.set_page_config(page_title="STRATEGIC INTEL HUB", layout="wide", initial_sidebar_state="collapsed")

# --- CSS מתקדם לעיצוב חללי (Glassmorphism & Cyber) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
    
    /* רקע ואנימציית רשת */
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(0deg, transparent 24%, rgba(0, 255, 65, .05) 25%, rgba(0, 255, 65, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 65, .05) 75%, rgba(0, 255, 65, .05) 76%, transparent 77%, transparent), 
                          linear-gradient(90deg, transparent 24%, rgba(0, 255, 65, .05) 25%, rgba(0, 255, 65, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 65, .05) 75%, rgba(0, 255, 65, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }

    /* כרטיסי נתונים מעוצבים */
    .intel-card {
        background: rgba(20, 20, 20, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 65, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .intel-card:hover {
        border-color: #00ff41;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
    }

    .metric-title { font-family: 'Orbitron', sans-serif; color: #888; font-size: 0.7rem; text-transform: uppercase; }
    .metric-value { font-family: 'JetBrains Mono', monospace; color: #00ff41; font-size: 1.5rem; font-weight: bold; }
    .critical-value { color: #ff003c; text-shadow: 0 0 10px #ff003c; }
    
    /* כותרות */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; color: #00ff41 !important; text-transform: uppercase; letter-spacing: 3px; }
    
    /* אנימציית פעימה לאינדיקטורים קריטיים */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    .status-pulse { animation: pulse 1.5s infinite; color: #ff003c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- חיבור ל-AI (Gemini) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# --- כותרת ראשית ---
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="margin: 0;">🛰️ OSINT COMMAND CENTER</h1>
        <p style="color: #00ff41; font-family: 'JetBrains Mono'; opacity: 0.7;">ENCRYPTED STRATEGIC FEED // UNIT 8200 STYLE</p>
    </div>
""", unsafe_allow_html=True)

# --- פונקציה לכרטיס גרפי ---
def intel_box(title, value, is_critical=False):
    style = "critical-value status-pulse" if is_critical else "metric-value"
    st.markdown(f"""
        <div class="intel-card">
            <div class="metric-title">{title}</div>
            <div class="{style}">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- חלוקת המסך ל-Grid של 24 אינדיקטורים ---
categories = {
    "📊 Markets": [("War Risk", "HIGH", True), ("Oil Bias", "$65.4", False), ("Polymarket", "82%", True), ("Rial (Black)", "621K", True), ("Kharg AIS", "SILENT", True)],
    "✈️ Aviation": [("ISR Fleet", "EVACUATED", False), ("ESCAT", "ACTIVE", True), ("IRN Flights", "GROUNDED", True), ("VIP Jets", "MASHHAD", False)],
    "⚔️ Military": [("USS Georgia", "RED SEA", True), ("KC-46 Hub", "SPIKE", True), ("B-2 Spirit", "DEPLOYED", True), ("Nuclear", "REINFORCED", True), ("IRGC Command", "OFFLINE", True)],
    "📡 Signals": [("Net Outage", "65%", True), ("GPS Jam", "LVL 5", True), ("Proxy Talk", "SILENT", False), ("SIGINT", "SPIKE", True), ("Cyber Scan", "CRITICAL", True)],
    "🌍 Diplomatic": [("Embassy", "EVACUATING", True), ("Witkoff", "DEPARTED", True), ("Decoy Model", "ACTIVE", False), ("Medical", "CODE RED", True)]
}

# תצוגת הקטגוריות בטורים
cols = st.columns(5)
all_indicators = [] # לאיסוף הנתונים עבור ה-AI

for i, (cat_name, items) in enumerate(categories.items()):
    with cols[i]:
        st.markdown(f"### {cat_name}")
        for label, val, crit in items:
            intel_box(label, val, crit)
            all_indicators.append(f"{label}: {val}")

st.markdown("<br>", unsafe_allow_html=True)

# --- גרפיקה חיה (Real-time chart) ---
st.subheader("📈 STRATEGIC TENSION INDEX (24H)")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['GPS Jamming', 'Market Panic', 'Military Comms']
).cumsum()
st.line_chart(chart_data)

# --- מנוע הניתוח המבצעי (Gemini) ---
st.divider()
st.subheader("⚡ TACTICAL ANALYSIS ENGINE")
if st.button("GENERATE STRATEGIC ESTIMATE"):
    if model:
        with st.spinner("Processing Global Signals..."):
            prompt = f"Analyze these signals: {', '.join(all_indicators)}. Provide a war probability estimate and a military-style summary in Hebrew."
            try:
                response = model.generate_content(prompt)
                st.markdown(f"""
                    <div style="background: rgba(255,0,60,0.1); border: 1px solid #ff003c; padding: 20px; border-radius: 5px; color: white;">
                        <h4 style="color: #ff003c;">[CLASSIFIED] AI ESTIMATE:</h4>
                        {response.text}
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Engine Error: {e}")
    else:
        st.error("AI Key Offline")

# לוגים תחתונים
st.subheader("📜 RECENT COMMS LOG")
st.code("""
[22:14] SIGINT: Encrypted traffic spike detected - Tehran to Beirut.
[21:55] IMINT: Thermal signatures confirmed at Fordow entrance.
[21:30] OSINT: Local reports of civilian evacuation in Southern Lebanon.
""", language="accesslog")
