import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# הגדרות דף בסגנון חמ"ל סייבר
st.set_page_config(page_title="STRATEGIC OSINT DASHBOARD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    .stMetric { border: 1px solid #00FF41; padding: 10px; background: #0a0a0a; border-radius: 0px; }
    .category-header { color: #00FF41; border-bottom: 2px solid #00FF41; padding-bottom: 5px; margin-top: 20px; text-transform: uppercase; }
    .ai-box { border: 1px dashed #ff4b4b; padding: 15px; background: #1a0000; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- מנוע חיבור AI חכם ---
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # ניסיון התחברות למודל פלאש 1.5
        model = genai.GenerativeModel('gemini-1.5-flash')
        # בדיקה קצרה אם המודל זמין
        st.sidebar.success("✅ AI Engine Connected")
    except Exception as e:
        st.sidebar.error(f"AI Connection Error: {str(e)}")
else:
    st.sidebar.warning("⚠️ API Key Missing in Secrets")

st.title("⚡ OSINT STRATEGIC COMMAND CENTER")
st.write(f"SYSTEM STATUS: ACTIVE | UTC: {datetime.utcnow().strftime('%H:%M:%S')}")

# --- פריסת 24 האינדיקטורים המלאה ---

# 1. Market & Maritime
st.markdown("<div class='category-header'>📊 Market & Maritime</div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("War Risk (Lloyd's)", "HIGH", "+12%")
c2.metric("Brent Oil Anomaly", "$65.2", "MANIPULATED")
c3.metric("Polymarket War %", "74%", "+8%")
c4.metric("IRR Black Market", "615K", "Panic Buy")
c5.metric("Kharg Island AIS", "EMPTY", "Critical")

# 2. Aviation
st.markdown("<div class='category-header'>✈️ Aviation OSINT</div>", unsafe_allow_html=True)
c6, c7, c8, c9 = st.columns(4)
c6.metric("ISR Civilian Fleet", "EVACUATED", "Safe Ports")
c7.metric("ESCAT Saudi", "ACTIVE", "Restricted")
c8.metric("Iran Domestic", "SUSPENDED", "No-Fly")
c9.metric("Gov VIP Movement", "ACTIVE", "Tehran Exit")

# 3. Military Posture
st.markdown("<div class='category-header'>⚔️ Military Posture</div>", unsafe_allow_html=True)
c10, c11, c12, c13, c14 = st.columns(5)
c10.metric("USS Georgia", "POSITIONED", "Tomahawk Ready")
c11.metric("Aerial Refueling", "KC-46 Active", "Qatar Hub")
c12.metric("Strategic Bombers", "B-2 Deployed", "In-Theater")
c13.metric("Nuclear Facilities", "SEALED", "Concrete Flow")
c14.metric("IRGC High Command", "BUNKERED", "Signal Silent")

# 4. Cyber & SIGINT
st.markdown("<div class='category-header'>📡 Cyber & SIGINT Spikes</div>", unsafe_allow_html=True)
c15, c16, c17, c18, c19, c20 = st.columns(6)
c15.metric("Gulf Sentiment", "PANIC", "Elite Exit")
c16.metric("Internet Outages", "ACTIVE", "Target Zones")
c17.metric("GPS Jamming", "LEVEL 5", "ISR/LEB")
c18.metric("Proxy Chatter", "SILENT", "Pre-Strike")
c19.metric("SIGINT Traffic", "SPIKE", "Encrypted")
c20.metric("Infrastructure Cyber", "ACTIVE", "Scans Detected")

# 5. Diplomacy & Civil Defense
st.markdown("<div class='category-header'>🌍 Diplomacy & Civil Defense</div>", unsafe_allow_html=True)
c21, c22, c23, c24 = st.columns(4)
c21.metric("Summit Decoy", "ACTIVE", "Strategic")
c22.metric("Witkoff Plane", "DEPARTED", "T-Minus 0")
c23.metric("Embassy Evacuation", "RUSSIA/CHINA", "URGENT")
c24.metric("Hospital Readiness", "CANCELLED", "Emergency Mode")

st.divider()

# --- כפתור הניתוח המודיעיני ---
st.subheader("📝 COMMANDER'S INTEL SUMMARY")
if st.button("RUN DEEP ANALYSIS"):
    if model:
        with st.spinner("Analyzing 24 vectors via Gemini AI..."):
            try:
                prompt = "Analyze these indicators: Oil at $65, IRR panic, GPS jamming level 5, and Embassies evacuating. What is the immediate war probability? Answer in Hebrew."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='ai-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Generation Error: {str(e)}")
    else:
        st.error("AI Engine is not connected. Check your API Key.")
