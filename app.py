import streamlit as st
import pickle
import numpy as np
import os

# 1. PAGE SETUP & CONFIGURATION
st.set_page_config(page_title="Stroke Risk Evaluator", page_icon="🧠", layout="centered")

# Initialize session state for multi-phase layout navigation
if 'app_phase' not in st.session_state:
    st.session_state.app_phase = "welcome"

# 2. LOAD ASSETS SAFELY (Logistic Regression & Scaler Only)
@st.cache_resource
def load_medical_assets():
    with open('stroke_logistic_model.pkl', 'rb') as f:
        lr = pickle.load(f)
    
    # Scaler is optional but highly recommended if numerical features were normalized
    sc = None
    if os.path.exists('stroke_scaler.pkl'):
        with open('stroke_scaler.pkl', 'rb') as f:
            sc = pickle.load(f)
    return lr, sc

try:
    logistic_model, stroke_scaler = load_medical_assets()
    st.sidebar.success("⚡ Diagnostic Engine Active!")
except FileNotFoundError:
    st.error("❌ Diagnostic File Error: 'stroke_logistic_model.pkl' not found. Please ensure it is uploaded to your GitHub repository.")
    st.stop()


# ==========================================
# PHASE 1: FRONT PHASE WELCOME LANDING
# ==========================================
if st.session_state.app_phase == "welcome":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #78281F; font-size: 40px;'>🧠 Stroke Risk Assessment Protocol</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5D6D7E; font-size: 18px;'>An advanced AI health screening tool to analyze vascular profiles, metabolic markers, and behavioral factors.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #FDEDEC; padding: 25px; border-radius: 12px; border: 1px solid #F5B7B1; text-align: center;'>
        <span style='font-size: 55px;'>❤️🩺📊</span>
        <h3 style='color: #78281F; margin-top: 12px;'>Begin Non-Invasive Cardiovascular Risk Analysis</h3>
        <p style='color: #7B7D7D;'>This system cross-references parameters against clinical diagnostic records using Logistic Regression to predict early anomaly detection indicators.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("🩺 Start Diagnostic Health Check", use_container_width=True):
        st.session_state.app_phase = "questionnaire"
        st.rerun()


# ==========================================
# PHASE 2: HEALTH QUESTIONNAIRE & RESULTS
# ==========================================
elif st.session_state.app_phase == "questionnaire":
    
    col_nav, col_title = st.columns([1, 6])
    with col_nav:
        if st.button("⬅️ Restart"):
            st.session_state.app_phase = "welcome"
            st.rerun()
            
    st.markdown("<h2 style='color: #78281F;'>📋 Patient Metric Questionnaire</h2>", unsafe_allow_html=True)
    st.markdown("Please key in the medical profile information precisely to assess vascular risk.")
    st.markdown("---")

    # SECTION 1: BIOLOGICAL & PHYSICAL MARKERS
    st.markdown("### 🧬 Biological & Physical Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        gender = st.selectbox("Biological Gender", options=["Female", "Male"])
        age = st.number_input("Patient Age (Years)", min_value=1, max_value=120, value=45, step=1)
    with col2:
        hypertension = st.selectbox("History of Hypertension?", options=["No", "Yes"])
        bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=60.0, value=28.5, step=0.1)
    with col3:
        heart_disease = st.selectbox("History of Heart Disease?", options=["No", "Yes"])
        glucose = st.number_input("Avg Glucose Level (mg/dL)", min_value=40.0, max_value=350.0, value=105.0, step=0.5)

    # SECTION 2: SOCIAL & LIFESTYLE PROFILE
    st.markdown("### 🚬 Socio-Environmental & Lifestyle Profile")
    col4, col5, col6 = st.columns(3)
    with col4:
        ever_married = st.selectbox("Ever Married?", options=["No", "Yes"])
    with col5:
        work_type = st.selectbox("Primary Employment Domain", options=["Private", "Self-employed", "Govt_job", "children"])
    with col6:
        residence = st.selectbox("Residence Environment Type", options=["Urban", "Rural"])

    smoking_status = st.selectbox("Smoking Habits Context", options=["never smoked", "formerly smoked", "smokes", "Unknown"])

    # 4. EXACT ALPHABETICAL ENCODING MAPS (Matching dataset columns training rules)
    gender_map = {"Female": 0, "Male": 1}
    married_map = {"No": 0, "Yes": 1}
    work_map = {"Govt_job": 0, "Private": 1, "Self-employed": 2, "children": 3}
    residence_map = {"Rural": 0, "Urban": 1}
    smoking_map = {"Unknown": 0, "formerly smoked": 1, "never smoked": 2, "smokes": 3}

    # Transform inputs to encoded labels
    gender_enc = gender_map[gender]
    married_enc = married_map[ever_married]
    work_enc = work_map[work_type]
    residence_enc = residence_map[residence]
    smoking_enc = smoking_map[smoking_status]
    hyper_enc = 1 if hypertension == "Yes" else 0
    heart_enc = 1 if heart_disease == "Yes" else 0

    # 5. CONSTRUCT EXACT MULTIDIMENSIONAL ELEMENT VECTOR
    raw_patient_features = [
        gender_enc, age, hyper_enc, heart_enc, married_enc,
        work_enc, residence_enc, glucose, bmi, smoking_enc
    ]

    st.markdown("<br>", unsafe_allow_html=True)

    # DIAGNOSTIC CALCULATION SUBMIT BUTTON
    if st.button("🔬 Execute AI Cardiovascular Diagnostics", use_container_width=True):
        try:
            input_array = np.array([raw_patient_features])
            
            # Process feature vectors through scaler array shapes if available
            if stroke_scaler is not None:
                if stroke_scaler.n_features_in_ == 10:
                    input_array = stroke_scaler.transform(input_array)
                elif stroke_scaler.n_features_in_ == 3:
                    scaled_nums = stroke_scaler.transform([[age, glucose, bmi]])[0]
                    input_array = np.array([[
                        gender_enc, scaled_nums[0], hyper_enc, heart_enc, married_enc,
                        work_enc, residence_enc, scaled_nums[1], scaled_nums[2], smoking_enc
                    ]])

            # Run Predictive Classification Check via Logistic Regression
            stroke_risk_prediction = logistic_model.predict(input_array)[0]

            st.markdown("---")
            # ==========================================
            # RENDER DIAGNOSTIC OUTPUT RESPONSES
            # ==========================================
            if stroke_risk_prediction == 1:
                st.markdown("""
                <div style='background-color: #FDEDEC; padding: 25px; border-radius: 12px; border-left: 8px solid #922B21;'>
                    <h2 style='color: #922B21; margin-top: 0;'>⚠️ Evaluation Alert: High Risk Detected</h2>
                    <p style='color: #2C3E50; font-size: 16px;'>The analytical engine reports metrics correlated heavily with high-risk classification zones.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # DYNAMIC HEALTH ADVISORY OUTLINE
                st.markdown("<br>", unsafe_allow_html=True)
                col_diet, col_exe = st.columns(2)
                
                with col_diet:
                    st.markdown("""
                    <div style='background-color: #FEF9E7; padding: 20px; border-radius: 10px; border-top: 4px solid #D4AC0D; min-height: 280px;'>
                        <h4 style='color: #7D6608; margin-top:0;'>🥗 Recommended Cardiovascular Diet Plan</h4>
                        <ul style='font-size: 14px; color: #2C3E50; padding-left: 20px;'>
                            <li><b>Sodium Restriction:</b> Lower salt intake to &lt; 1,500mg daily to stabilize arterial blood pressure wall strain.</li>
                            <li><b>DASH Diet Layout:</b> Prioritize heavy leafy vegetables, whole grain profiles, and lean poultry proteins.</li>
                            <li><b>Vascular Protection:</b> Introduce high Omega-3 fatty acids (flaxseeds, walnuts, olive oil compounds).</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_exe:
                    st.markdown("""
                    <div style='background-color: #EAF2F8; padding: 20px; border-radius: 10px; border-top: 4px solid #2980B9; min-height: 280px;'>
                        <h4 style='color: #1B4F72; margin-top:0;'>🏃‍♀️ Regulated Vascular Exercise Routine</h4>
                        <ul style='font-size: 14px; color: #2C3E50; padding-left: 20px;'>
                            <li><b>LISS Cardio:</b> 30 minutes of Low-Intensity Steady-State exercise (brisk walking, cycling) 5 days a week.</li>
                            <li><b>Arterial Expansion:</b> Avoid heavy unassisted weight lifting to prevent rapid spike changes in pressure.</li>
                            <li><b>Pacing Mandate:</b> Stop activities immediately if dizziness, shortness of breath, or chest tension develops.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
            else:
                st.markdown("""
                <div style='background-color: #EAF2F8; padding: 25px; border-radius: 12px; border-left: 8px solid #1F618D; text-align: center;'>
                    <h2 style='color: #1F618D; margin-top: 0;'>✅ Evaluation Profile: Low / Standard Risk</h2>
                    <p style='color: #2C3E50; font-size: 16px; margin-bottom: 0;'>The clinical data array charts within traditional benchmark safezones via the execution engine.</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"🚨 Diagnostic Pipeline Anomaly Encountered: {e}")