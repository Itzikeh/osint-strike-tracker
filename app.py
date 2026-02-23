import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import google.generativeai as genai
from datetime import datetime

# הגדרות דף - DEFCON UI
st.set_page_config(page_title="DEFCON OSINT TRACKER", layout="wide", initial_sidebar_state="collapsed")

# --- הזרקת CSS מטורף לחיקוי ה-React UI ששלחת ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500;800&family=Orbitron:wght@400;900&display=swap');
    
    body { background-color: #020305; color: #f0f6fc; }
    .stApp { background: #020305; }
    
    /* כותרת HUD */
    .hud-header {
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 20px 0;
        margin-bottom: 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .hud-title { font-family: 'Orbitron', sans-serif; font-weight: 900; letter-spacing: -1px; font-size: 2rem; color: #fff; }
    .node-id { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #444; letter-spacing: 2px; }

    /* כרטיסיות אינדיקטורים */
    .matrix-card {
        background: rgba(8, 11, 18, 0.5);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 25px;
        transition: 0.3s;
        margin-bottom: 15px;
    }
    .matrix-card:hover { border-color: rgba(239, 68, 68, 0.4); background: rgba(8, 11, 18, 0.8); }
    
    .label { font-family: 'JetBrains Mono'; font-size: 0.65rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
    .value-text { font-family: 'JetBrains Mono'; font-size: 1.4rem; font-weight: 800; color: #fff; margin-top: 5px; }
    .percent { font-size: 0.8rem; color: #3b82f6; }
    .critical { color: #ef4444 !important; }

    /* שעון הסתברות מרכזי */
    .prob-box {
        background: #080b12;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 40px;
        padding: 60px 20px;
        text-align: center;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    .prob-value { font-family: 'JetBrains Mono'; font-size: 8rem; font-weight: 900; line-height: 1; color: #fff; }
    
    /* כפתור AI */
    .stButton>button {
        background: #4f46e5;
        color: white;
        border-radius: 15px;
        padding: 20px;
        font-family: 'Orbitron';
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #6366f1; box-shadow: 0 0 20px rgba(79, 70, 229, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- פונקציית AI משודרגת ---
def run_strategic_analysis(indicators):
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Analyze these 24 indicators: {indicators}. 
        1. Determine the EXACT probability (%) of war in the next 72 hours.
        2. Write a 3-sentence military intelligence brief in Hebrew.
        3. Identify the 'Tipping Point' indicator.
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except: return "AI Engine Offline"
    return "No API Key Found"

# --- HUD Header ---
st.markdown("""
    <div class="hud-header">
        <div>
            <div class="hud-title">DEFCON TRACKER</div>
            <div class="node-id">NODE: OSINT-ISR-01 // SECURITY LEVEL: ELEVATED</div>
        </div>
        <div style="text-align: right;">
            <div style="color: #ef4444; font-weight: bold; font-family: 'JetBrains Mono'; font-size: 0.8rem;">● LIVE DATA SYNC</div>
            <div class="node-id">MODEL: GEMINI-1.5-FLASH</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- לוגיקת נתונים ---
# (כאן בעתיד נחבר APIs, כרגע זה מדמה נתונים חיים)
data = {
    "Military": [("USS Georgia", 85), ("Tanker Bridge", 70), ("B-52 Assets", 90), ("Bunker Ops", 45), ("IRGC Signal", 78)],
    "Markets": [("War Risk", 65), ("Brent Crude", 22), ("Polymarket", 82), ("Rial Crash", 55), ("Kharg AIS", 95)],
    "Aviation": [("ISR Fleet", 40), ("ESCAT Proc", 10), ("IRN Cancels", 88), ("VIP Flights", 72)],
    "Cyber/SIG": [("GPS Jamming", 92), ("Net Blackout", 30), ("Proxy Chatter", 60), ("SIGINT Spike", 85), ("Cyber Waves", 50)],
    "Diplomacy": [("Witkoff Plane", 100), ("Embassy Evac", 90), ("Hosp. Alert", 60), ("Summit Decoy", 40)]
}

# --- Dashboard Layout ---
col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.markdown("<div class='prob-box'>", unsafe_allow_html=True)
    st.markdown("<div class='label'>Escalation Probability</div>", unsafe_allow_html=True)
    st.markdown("<div class='prob-value'>84<span style='font-size: 2rem; color: #333;'>%</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #ef4444; font-family: JetBrains Mono; font-size: 0.7rem; margin-top: 20px;'>WAR WINDOW DETECTED (72H)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("GENERATE AI SITREP"):
        all_ind = [f"{k}: {v}%" for cat in data.values() for k, v in cat]
        report = run_strategic_analysis(all_ind)
        st.info(report)

with col_right:
    # יצירת גריד של כרטיסיות
    cat_cols = st.columns(3)
    idx = 0
    for cat_name, items in data.items():
        with cat_cols[idx % 3]:
            st.markdown(f"<div style='font-family: Orbitron; color: #3b82f6; font-size: 0.8rem; margin-bottom: 15px;'>{cat_name.upper()}</div>", unsafe_allow_html=True)
            for label, val in items:
                crit_class = "critical" if val > 80 else ""
                st.markdown(f"""
                    <div class="matrix-card">
                        <div class="label">{label}</div>
                        <div class="value-text {crit_class}">{val}<span class="percent">%</span></div>
                    </div>
                """, unsafe_allow_html=True)
        idx += 1

# --- Footer ---
st.markdown("<div style='opacity: 0.1; font-family: JetBrains Mono; font-size: 0.6rem; text-align: center; margin-top: 50px;'>CIPHER: AES-512 // STATUS: ENCRYPTED // NO LOG RETAINED</div>", unsafe_allow_html=True)
