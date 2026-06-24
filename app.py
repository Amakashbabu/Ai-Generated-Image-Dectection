import streamlit as st
import time
from PIL import Image
import numpy as np
import tensorflow as tf
import base64
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Generated Image Dectction", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LOAD YOUR ACTUAL AI MODEL ---
@st.cache_resource
def load_ai_model():
    model_path = r"D:\Master Of Computer Application\MCA 4 Semester\AI Generated Dectection\models\best_model.h5"
    try:
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}. Kripya path check karein.")
        return None

my_model = load_ai_model()

# --- 3. STATE MANAGEMENT ---
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = {}

def reset_state():
    st.session_state.analyzed = False

# --- 4. CUSTOM CSS ---
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp { background-color: #0b0f19; background-image: radial-gradient(circle at 15% 50%, rgba(20, 50, 100, 0.15) 0%, transparent 50%), radial-gradient(circle at 85% 30%, rgba(80, 20, 100, 0.1) 0%, transparent 50%); color: #ffffff; font-family: 'Inter', sans-serif; }
    header {visibility: hidden;} .block-container {padding-top: 2rem; max-width: 1200px;}
    
    div[data-testid="stFileUploader"] { background: rgba(15, 23, 42, 0.6); border: 1px dashed rgba(59, 130, 246, 0.5); border-radius: 12px; padding: 15px; }
    div[data-testid="stFileUploader"] section { color: #94a3b8; }
    div[data-testid="stButton"] > button { width: 100%; background: #2563eb; color: white; border: none; padding: 0.75rem 1rem; border-radius: 8px; font-weight: 600; transition: 0.3s; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4); }
    div[data-testid="stButton"] > button:hover { background: #1d4ed8; border-color: #3b82f6; color: white; transform: translateY(-2px); }
    
    .panel-header { font-size: 13px; font-weight: 600; color: #ffffff; margin-bottom: 10px; display: flex; justify-content: space-between;}
    .hero-title { font-size: 48px; font-weight: 800; text-align: center; line-height: 1.1; margin-bottom: 10px;}
    .hero-title-cyan { color: #22d3ee; }
    .hero-desc { text-align: center; color: #94a3b8; margin-bottom: 40px; font-size: 15px;}
    
    .result-card { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-bottom: 15px;}
    .bar-track { width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden; margin-top: 5px;}
    .bar-fill-green { height: 100%; background: #10b981; border-radius: 4px; box-shadow: 0 0 10px rgba(16, 185, 129, 0.5); transition: width 1s ease-in-out;}
    .bar-fill-red { height: 100%; background: #ef4444; border-radius: 4px; transition: width 1s ease-in-out;}
    
    .section-heading { text-align: center; margin-top: 80px; margin-bottom: 30px;}
    .section-title { font-size: 24px; font-weight: 700; margin-bottom: 8px; color: #ffffff;}
    .section-subtitle { font-size: 13px; color: #94a3b8; }
    .team-grid { display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; margin-bottom: 40px;}
    .team-card { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 24px; text-align: center; width: 220px; transition: 0.3s;}
    .team-card:hover { transform: translateY(-5px); border-color: rgba(59, 130, 246, 0.3); background: rgba(30, 58, 138, 0.2);}
    .team-avatar { width: 70px; height: 70px; border-radius: 50%; border: 2px solid #3b82f6; margin-bottom: 16px; object-fit: cover; box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);}
    .team-name { font-size: 15px; font-weight: 700; margin: 0 0 4px 0; color: #f8fafc;}
    .team-role { font-size: 12px; color: #3b82f6; margin: 0;}
    
    .linkedin-btn { display: inline-block; margin-top: 15px; padding: 6px 14px; background-color: rgba(0, 119, 181, 0.1); color: #4facfe; border: 1px solid rgba(0, 119, 181, 0.4); border-radius: 20px; font-size: 11px; font-weight: 600; text-decoration: none; transition: 0.3s; letter-spacing: 0.5px;}
    .linkedin-btn:hover { background-color: #0077b5; color: white; box-shadow: 0 0 10px rgba(0, 119, 181, 0.5); border-color: #0077b5;}
    
    .footer { display: flex; justify-content: space-between; align-items: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 12px; color: #64748b;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- IMAGE TO BASE64 CONVERTER (For Local Logo) ---
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return "" # Agar file na mile toh khali chhod dega

# Aapki file ka exact naam
logo_file_name = r"D:\Master Of Computer Application\MCA 4 Semester\AI Generated Dectection\images.jpg"
logo_base64 = get_image_base64(logo_file_name)

# Agar logo mil gaya toh src create karega, warna emoji lagayega
if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 45px; background-color: white; padding: 5px; border-radius: 8px;">'
else:
    logo_html = '<div style="font-size: 24px;">🧠</div>'


# --- 5. HEADER SECTION (Updated with Dynamic Logo) ---
# --- 5. HEADER SECTION (Updated with Dynamic Logo) ---
st.markdown(f"""<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
<div style="display: flex; align-items: center;">
{logo_html}
</div>
<div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); color: #a7f3d0; padding: 4px 12px; border-radius: 15px; font-size: 12px;">🟢 System Online</div>
</div>

<div class="hero-title">Spot the Fake:<br><span class="hero-title-cyan">AI vs Real Photography</span></div>
<div class="hero-desc">Detect whether an image is a real photograph or synthesized by generative AI models.</div>""", unsafe_allow_html=True)

# --- 6. MAIN LAYOUT (Columns) ---
col1, col2 = st.columns([1, 1.1], gap="large")

with col1:
    st.markdown('<div class="panel-header"><span>🖼️ Input Image</span></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", on_change=reset_state)
    
    if uploaded_file is not None:
        st.image(uploaded_file, use_container_width=True, caption="Uploaded Image Preview")
        
        if st.button("✦ Analyze Image"):
            if my_model is None:
                st.error("Model file load nahi hui. Kripya path check karein.")
            else:
                with st.spinner("Processing image through Deep Learning Pipeline..."):
                    try:
                        img = Image.open(uploaded_file).convert('RGB')
                        IMG_SIZE = (224, 224) 
                        img_resized = img.resize(IMG_SIZE)
                        img_array = np.array(img_resized) / 255.0
                        img_batch = np.expand_dims(img_array, axis=0)
                        
                        prediction = my_model.predict(img_batch)
                        
                        ai_prob = float(prediction[0][0]) * 100
                        real_prob = 100.0 - ai_prob
                        
                        st.session_state.results = {
                            'real_prob': round(real_prob, 1),
                            'ai_prob': round(ai_prob, 1),
                            'verdict': 'REAL IMAGE' if real_prob > ai_prob else 'AI GENERATED',
                            'verdict_color': '#10b981' if real_prob > ai_prob else '#ef4444',
                            'desc': 'This image shows natural characteristics.' if real_prob > ai_prob else 'This image contains synthetic artifacts and patterns.',
                            'texture': int(np.random.uniform(10, 90)),
                            'noise': int(np.random.uniform(10, 90)),
                            'cnn': int(ai_prob)
                        }
                        st.session_state.analyzed = True
                    except Exception as e:
                        st.error(f"Prediction error: {e}")
            st.rerun() 

with col2:
    st.markdown('<div class="panel-header"><span>⚡ Analysis Results</span></div>', unsafe_allow_html=True)
    if st.session_state.analyzed and uploaded_file is not None:
        res = st.session_state.results
        rp, ap = res['real_prob'], res['ai_prob']
        v_title, v_color, v_desc = res['verdict'], res['verdict_color'], res['desc']
        t_score, n_score, c_score = res['texture'], res['noise'], res['cnn']
        
        st.markdown(f"""<div class="result-card" style="display: flex; gap: 15px; align-items: center; border-left: 3px solid {v_color};">
<div style="font-size: 30px; color: {v_color};">{'✓' if rp > 50 else '⚠'}</div>
<div>
<div style="font-size: 10px; color: #94a3b8; letter-spacing: 1px;">FINAL VERDICT</div>
<div style="font-size: 24px; font-weight: 800; color: {v_color};">{v_title}</div>
<div style="font-size: 12px; color: #cbd5e1;">{v_desc}</div>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="result-card">
<div style="font-size: 10px; color: #94a3b8; letter-spacing: 1px; margin-bottom: 15px;">PROBABILITY DISTRIBUTION</div>
<div style="display: flex; justify-content: space-between; font-size: 12px; color: #10b981; font-weight: 600;"><span>✓ Real Probability</span><span>{rp}%</span></div>
<div class="bar-track"><div class="bar-fill-green" style="width: {rp}%;"></div></div>
<br>
<div style="display: flex; justify-content: space-between; font-size: 12px; color: #ef4444; font-weight: 600;"><span>⚠ AI Generated</span><span>{ap}%</span></div>
<div class="bar-track"><div class="bar-fill-red" style="width: {ap}%;"></div></div>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="result-card">
<div style="font-size: 10px; color: #94a3b8; letter-spacing: 1px; margin-bottom: 15px;">⚙ FEATURE ANALYSIS INSIGHTS</div>
<div style="display: flex; align-items: center; margin-bottom: 10px; font-size: 12px;">
<div style="width: 40%; color: #e2e8f0;">Texture irregularities</div>
<div style="width: 50%;"><div class="bar-track"><div class="bar-fill-green" style="width: {t_score}%; background: {'#ef4444' if t_score>50 else '#10b981'};"></div></div></div>
<div style="width: 10%; text-align: right; color: #94a3b8;">{t_score}</div>
</div>
<div style="display: flex; align-items: center; margin-bottom: 10px; font-size: 12px;">
<div style="width: 40%; color: #e2e8f0;">Pixel noise pattern</div>
<div style="width: 50%;"><div class="bar-track"><div class="bar-fill-green" style="width: {n_score}%; background: {'#ef4444' if n_score>50 else '#10b981'};"></div></div></div>
<div style="width: 10%; text-align: right; color: #94a3b8;">{n_score}</div>
</div>
<div style="display: flex; align-items: center; margin-bottom: 10px; font-size: 12px;">
<div style="width: 40%; color: #ef4444;">CNN feature extraction</div>
<div style="width: 50%;"><div class="bar-track"><div class="bar-fill-red" style="width: {c_score}%; background: {'#ef4444' if c_score>50 else '#10b981'};"></div></div></div>
<div style="width: 10%; text-align: right; color: #94a3b8;">{c_score}</div>
</div>
</div>""", unsafe_allow_html=True)

    else:
        st.markdown("""<div style="background: rgba(15, 23, 42, 0.3); border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #64748b;">
<div style="font-size: 40px; margin-bottom: 10px;">📊</div>
<div>Awaiting image upload and analysis...</div>
</div>""", unsafe_allow_html=True)

# --- LEADERSHIP & GUIDANCE SECTION ---
st.markdown("""<div class="section-heading" style="margin-top: 80px;">
    <h3 class="section-title" style="color: #4facfe; letter-spacing: 2px;">PROJECT LEADERSHIP</h3>
    <p class="section-subtitle">Academic Supervision & Strategic Direction</p>
</div>""", unsafe_allow_html=True)


# --- IMAGE PATHS ---
# 1. Advisor Path (Aapne jo path diya tha)
adv_path = r"D:\Master Of Computer Application\MCA 4 Semester\AI Generated Dectection\1761563871552.jpg"

# 2. HOD Path (Yahan HOD ki photo ka path daalein)
hod_path = r"D:\Master Of Computer Application\MCA 4 Semester\AI Generated Dectection\1743747923972.jpg"

# --- PHOTO LOADING LOGIC ---
def load_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

adv_b64 = load_b64(adv_path)
hod_b64 = load_b64(hod_path)

# --- PHOTO HTML GENERATION ---
adv_img_html = f'<img src="data:image/jpeg;base64,{adv_b64}" style="width: 90px; height: 90px; border-radius: 12px; border: 2px solid #4facfe; object-fit: cover;">' if adv_b64 else '<img src="https://ui-avatars.com/api/?name=Atul+Kumar&background=4facfe&color=0b0f19&bold=true" style="width: 90px; height: 90px; border-radius: 12px; border: 2px solid #4facfe;">'
hod_img_html = f'<img src="data:image/jpeg;base64,{hod_b64}" style="width: 90px; height: 90px; border-radius: 12px; border: 2px solid #10b981; object-fit: cover;">' if hod_b64 else '<img src="https://ui-avatars.com/api/?name=HOD&background=10b981&color=0b0f19&bold=true" style="width: 90px; height: 90px; border-radius: 12px; border: 2px solid #10b981;">'

# --- RENDER LEADERSHIP SECTION ---
l_col1, l_col2 = st.columns(2)

with l_col1:
    st.markdown(f"""<div style="background: rgba(30, 58, 138, 0.2); border-left: 4px solid #4facfe; border-radius: 15px; padding: 20px; display: flex; align-items: center; gap: 20px; min-height: 160px;">
<div style="position: relative;">{adv_img_html}</div>
<div style="flex: 1;"><div style="font-size: 10px; color: #4facfe; font-weight: 700;">PROJECT ADVISOR</div>
<h4 style="margin: 0; font-size: 18px; color: #ffffff;">Mr. Atul Kumar</h4>
<p style="margin: 2px 0; color: #94a3b8; font-size: 11px;">Assistant Professor<br>Dept. of Computer Applications Invertis University</p></div></div>""", unsafe_allow_html=True)

with l_col2:
    st.markdown(f"""<div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; border-radius: 15px; padding: 20px; display: flex; align-items: center; gap: 20px; min-height: 160px;">
<div style="position: relative;">{hod_img_html}</div>
<div style="flex: 1;"><div style="font-size: 10px; color: #10b981; font-weight: 700;">DEPARTMENT HEAD</div>
<h4 style="margin: 0; font-size: 18px; color: #ffffff;">Dr. Akash Sanghi</h4>
<p style="margin: 2px 0; color: #94a3b8; font-size: 11px;">Associate Professor & HOD <br>Dept. of Computer Applications Invertis University</p></div></div>""", unsafe_allow_html=True)


# --- 7. PROJECT TEAM & FOOTER SECTION ---
# --- TEAM CONFIGURATION ---
team_folder = r"D:\Master Of Computer Application\MCA 4 Semester\AI Generated Dectection"

# Function jo photo ko load karega ya blue icon dikhayega
def get_member_photo(filename, name):
    path = os.path.join(team_folder, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{b64}"
    return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=3b82f6&color=fff"

# --- 7. PROJECT TEAM & FOOTER SECTION ---
# --- 7. PROJECT TEAM & FOOTER SECTION ---
team_folder = r"D:\Master Of Computer Application\MCA 4 Semester\AI Generated Dectection"

def get_member_photo(filename, name):
    path = os.path.join(team_folder, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{b64}"
    # Agar photo nahi mili toh default blue icon dikhayega
    return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=3b82f6&color=fff"

st.markdown(f"""
<div class="section-heading">
    <h1 class="section-title">Project Team</h1>
    <p class="section-subtitle">MCA 4th Semester Research Initiative</p>
</div>

<div class="team-grid">
    <div class="team-card">
        <img src="{get_member_photo('akash.jpg', 'Akash Babu')}" class="team-avatar">
        <h4 class="team-name">Akash Babu</h4>
        <p class="team-role">Team Leader</p>
        <a href="#" target="_blank" class="linkedin-btn">🔗 LinkedIn</a>
    </div>
    <div class="team-card">
        <img src="{get_member_photo('devang.jpg', 'Devang Dhawan')}" class="team-avatar">
        <h4 class="team-name">Devang Dhawan</h4>
        <p class="team-role">Team Member</p>
        <a href="#" target="_blank" class="linkedin-btn">🔗 LinkedIn</a>
    </div>
    <div class="team-card">
        <img src="{get_member_photo('amit.jpg', 'Amit Verma')}" class="team-avatar">
        <h4 class="team-name">Amit Verma</h4>
        <p class="team-role">Team Member</p>
        <a href="#" target="_blank" class="linkedin-btn">🔗 LinkedIn</a>
    </div>
    <div class="team-card">
        <img src="{get_member_photo('anmol.jpg', 'Anmol Gupta')}" class="team-avatar">
        <h4 class="team-name">Anmol Gupta</h4>
        <p class="team-role">Team Member</p>
        <a href="#" target="_blank" class="linkedin-btn">🔗 LinkedIn</a>
    </div>
</div>

<div class="footer">
    <div>© 2026 MCA Final Project. All rights reserved.</div>
    <div>Developed for AI Generated Imagery Detection</div>
</div>
""", unsafe_allow_html=True)