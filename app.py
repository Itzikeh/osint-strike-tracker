import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# הגדרות עיצוב מתקדמות
st.set_page_config(page_title="STRATEGIC OSINT DASHBOARD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    .stMetric { border: 1px solid #00FF41; padding: 10px; background: #0a0a0a; border-radius: 0px; }
    .category-header { color: #00FF41; border-bottom: 2px solid #00FF41; padding-bottom: 5px; margin-top: 20px; text-transform: uppercase; letter-spacing: 2px; }
    .ai-box { border: 1px dashed #ff4b4b; padding: 15px; background: #1a0000; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# חיבור ל-Gemini
model = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: pass

st.title("⚡ OSINT STRATEGIC COMMAND CENTER")
st.write(f"SYSTEM STATUS: ACTIVE | UTC: {datetime.utcnow().strftime('%H:%M:%S')} | LOCATION: MIDDLE EAST")

# --- פריסת 24 האינדיקטורים ---

# קבוצה 1: כלכלה, שווקים וספנות
st.markdown("<div class='category-header'>📊 Market & Maritime Intel</div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("War Risk (Lloyd's)", "High", "+12%")
c2.metric("Brent Oil Anomaly", "$65.2", "MANIPULATED")
c3.metric("Polymarket War %", "74%", "+8%")
c4.metric("IRR Black Market", "615K", "Panic Buy")
c5.metric("Kharg Island AIS", "EMPTY", "Critical")

# קבוצה 2: תעופה אזרחית (Aviation OSINT)
st.markdown("<div class='category-header'>✈️ Aviation & Airspace</div>", unsafe_allow_html=True)
c6, c7, c8, c9 = st.columns(4)
c6.metric("ISR Civilian Fleet", "EVACUATED", "Safe Ports")
c7.metric("ESCAT Saudi", "ACTIVE", "NOTAM Restricted")
c8.metric("Iran Domestic Flights", "SUSPENDED", "Clear Skies")
c9.metric("Gov VIP Movement", "ACTIVE", "Tehran -> Mashhad")

# קבוצה 3: סדר כוחות (Military Posture)
st.markdown("<div class='category-header'>⚔️ Military Assets & Posture</div>", unsafe_allow_html=True)
c10, c11, c12, c13, c14 = st.columns(5)
c10.metric("USS Georgia", "IN POSITION", "Tomahawk Ready")
c11.metric("Aerial Refueling", "KC-46 Active", "Qatar Hub")
c12.metric("Strategic Bombers", "B-2 Deployed", "Diego Garcia")
c13.metric("Nuclear Facilities", "CONCRETE SEAL", "Maxar Intel")
c14.metric("IRGC Leadership", "BUNKERED", "Signal Silent")

# קבוצה 4: מודיעין רשת וסייבר (Cyber & SIGINT)
st.markdown("<div class='category-header'>📡 Cyber & SIGINT Spikes</div>", unsafe_allow_html=True)
c15, c16, c17, c18, c19, c20 = st.columns(6)
c15.metric("Gulf Social Sentiment", "PANIC", "Elite Exit")
c16.metric("Internet Blackouts", "ACTIVE", "Fordow/Natanz")
c17.metric("GPS Jamming", "LEVEL 5", "Israel/Lebanon")
c18.metric("Proxy Chatter", "SILENT", "Pre-strike Signal")
c19.metric("SIGINT Traffic", "SPIKE", "Encrypted")
c20.metric("Pre-kinetic Cyber", "ACTIVE", "Water/Grid Target")

# קבוצה 5: דיפלומטיה ועורף
st.markdown("<div class='category-header'>🌍 Diplomacy & Civil Defense</div>", unsafe_allow_html=True)
c21, c22, c23, c24 = st.columns(4)
c21.metric("Summit Decoy", "ACTIVE", "Strategic Deception")
c22.metric("Witkoff Plane", "DEPARTED", "T-Minus 0")
c23.metric("Embassy Evac", "CHINA/RUSSIA", "Urgent")
c24.metric("Hospital Prep", "ELECTIVE CANCEL", "Mass Casualty")

st.divider()

# --- מנוע הניתוח המרכזי ---
st.subheader("📝 COMMANDER'S INTEL SUMMARY (GEMINI AI)")
if st.button("RUN DEEP ANALYSIS"):
    if model:
        with st.spinner("Analyzing 24 vectors..."):
            prompt = "נתח את כל 24 האינדיקטורים המופיעים בדאשבורד. האם אנחנו במצב של מלחמה בשעות הקרובות? תן הערכת זמן ותעדוף איומים. ענה בפורמט צבאי קשיח."
            try:
                response = model.generate_content(prompt)
                st.markdown(f"<div class='ai-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Engine Failure: {str(e)}")
    else:
        st.error("API Key Not Found. Check Streamlit Secrets.")
