import streamlit as st
import json
import pandas as pd
from PIL import Image
from utils.vision_tools import process_image, mock_predict
from utils.geo_tools import find_nearest_miller
from utils.market_tools import negotiate_price

# --- 1. INITIALIZATION & CONFIG ---
st.set_page_config(page_title="KilimoSmart Maize", page_icon="🌽", layout="centered")

# Initialize Session State
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'lang' not in st.session_state:
    st.session_state.lang = "en"

# --- 2. MULTILINGUAL SETUP ---
def load_labels():
    with open('assets/sw_labels.json', 'r', encoding='utf-8') as f:
        return json.load(f)

labels = load_labels()

# Sidebar Settings
st.sidebar.title("⚙️ Mipangilio / Settings")
lang_toggle = st.sidebar.radio("Chagua Lugha / Select Language", ["English", "Kiswahili"])
st.session_state.lang = "en" if lang_toggle == "English" else "sw"
t = labels[st.session_state.lang]

# --- 3. UI HEADER ---
st.title(t["title"])
st.markdown(f"*{'Maize specialized AI for Kenyan Farmers' if st.session_state.lang == 'en' else 'AI maalum kwa wakulima wa mahindi nchini Kenya'}*")
st.divider()

# --- 4. LOCATION & GPS ---
st.header(t["location_header"])
col1, col2 = st.columns([1, 1])

with col1:
    if st.button(t["detect_loc"]):
        # Mocking GPS for prototype. In production, use streamlit-js-eval or streamlit-geolocation
        st.session_state['user_lat'] = -1.2995 
        st.session_state['user_lon'] = 36.8400
        st.success("📍 Trans-Nzoia Detected")

with col2:
    counties = ["Uasin Gishu", "Trans-Nzoia", "Nakuru", "Bungoma", "Kakamega", "Kiambu"]
    user_county = st.selectbox(t["county_fallback"], counties)

# --- 5. IMAGE INPUT & DIAGNOSIS ---
st.header(t["upload_header"])
tab1, tab2 = st.tabs([t["take_photo"], t["upload_file"]])

with tab1:
    cam_image = st.camera_input("Scanner")
with tab2:
    uploaded_image = st.file_uploader(t["upload_file"], type=['jpg', 'jpeg', 'png'])

active_image = cam_image or uploaded_image

if active_image:
    img = Image.open(active_image)
    st.image(img, caption="Preview", use_container_width=True)
    
    if st.button(t["analyze_btn"]):
        with st.spinner('Uchunguzi unaendelea... (Analyzing)'):
            # Process & Run Mock AI
            processed_img = process_image(active_image)
            disease, confidence = mock_predict(processed_img)
            
            if disease == "Rejected":
                st.error("❌ Picha haijatambuliwa. Tafadhali jaribu tena.")
                st.session_state.analysis_done = False
            else:
                st.session_state.analysis_done = True
                st.session_state.results = {"disease": disease, "confidence": confidence}

# --- 6. PERSISTENT RESULTS & MARKET ---
if st.session_state.analysis_done:
    res = st.session_state.results
    
    # Load Treatment Info
    with open('data/treatments.json', 'r') as f:
        treatments = json.load(f)
    
    info = treatments[res["disease"]]
    disease_name = info["sw_name"] if st.session_state.lang == "sw" else res["disease"]
    
    # Show Diagnosis Result
    st.success(f"✅ {disease_name} ({res['confidence']*100:.0f}%)")
    
    # Technical Advice
    with st.expander("📖 " + ("Treatment Advice" if st.session_state.lang == "en" else "Ushauri wa Matibabu")):
        st.write(f"**{'Medication' if st.session_state.lang == 'en' else 'Dawa'}:** {info['medication']}")
        st.write(f"**{'Prevention' if st.session_state.lang == 'en' else 'Kuzuia'}:** {info['prevention']}")

    st.divider()

    # Market Logic
    st.header(t["market_header"])
    
    # Find Miller using GPS
    lat = st.session_state.get('user_lat', -1.2995)
    lon = st.session_state.get('user_lon', 36.8400)
    miller = find_nearest_miller(lat, lon)
    
    # Quality-Based Negotiation
    grade, final_price, explain = negotiate_price(miller['base_price_kes'], res["disease"])
    
    # Offer Card
    st.subheader(f"🤝 {miller['name']}")
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Price (90kg Bag)", f"KES {final_price}", delta=f"Grade {grade}")
    m_col2.write(f"📍 {miller['location']}\n📞 {miller['contact']}")
    
    st.info(f"💡 {explain}")

    # The Final Action (M-Pesa Integration Point)
    if st.button("💰 " + ("Accept & Request Deposit" if st.session_state.lang == "en" else "Kubali na Omba Malipo")):
        st.balloons()
        st.warning("📲 Safaricom M-Pesa: Requesting STK Push...")
        # Placeholder for Daraja API call
        st.success(f"Payment request for 10% deposit sent to farmer's phone. Contacting {miller['name']} to arrange transport.")
        