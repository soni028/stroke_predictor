import streamlit as st
import pickle
import numpy as np
import os

# 1. PAGE SETUP & CONFIGURATION
st.set_page_config(page_title="Stroke Risk Evaluator", page_icon="🧠", layout="centered")

if 'app_phase' not in st.session_state:
    st.session_state.app_phase = "welcome"

# 2. LOAD ASSETS
@st.cache_resource
def load_medical_assets():
    with open('stroke_logistic_model.pkl', 'rb') as f:
        lr = pickle.load(f)
    sc = None
    if os.path.exists('stroke_scaler.pkl'):
        with open('stroke_scaler.pkl', 'rb') as f:
            sc = pickle.load(f)
    return lr, sc

try:
    logistic_model, stroke_scaler = load_medical_assets()
    st.sidebar.success("⚡ Diagnostic Engine Active!")
except FileNotFoundError:
    st.error("❌ Diagnostic File Error: 'stroke_logistic_model.pkl' not found.")
    st.stop()

# PHASE 1: FRONT PHASE WELCOME LANDING
if st.session_state.app_phase == "welcome":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #78281F; font-size: 40px;'>🧠 Stroke Risk Assessment Protocol</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5D6D7E; font-size: 18px;'>An advanced AI health screening tool to analyze vascular profiles and metabolic markers.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #FDEDEC; padding: 25px; border-radius: 12px; border: 1px solid #F5B7B1; text-align: center;'>
        <span style='font-size: 55px;'>❤️🩺📊</span>
        <h3 style='color: #78281F; margin-top: 12px;'>Begin Non-Invasive Risk Analysis</h3>
        <p style='color: #7B7D7D;'>Cross-references patient parameters using Logistic Regression to predict target safety boundaries.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("🩺 Start Diagnostic Health Check", use_container_width=True):
        st.session_state.app_phase = "questionnaire"
        st.rerun()

# PHASE 2: HEALTH QUESTIONNAIRE & RESULTS
elif st.session_state.app_phase == "questionnaire":
    col_nav, _ = st.columns([1, 6])
    with col_nav:
        if st.button("⬅️ Restart"):
            st.session_state.app_phase = "welcome"
            st.rerun()
            
    st.markdown("<h2 style='color: #78281F;'>📋 Patient Metric Questionnaire</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # BIOLOGICAL & PHYSICAL MARKERS INPUTS
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

    # SOCIAL & LIFESTYLE PROFILE INPUTS
    col4, col5, col6 = st.columns(3)
    with col4: ever_married = st.selectbox("Ever Married?", options=["No", "Yes"])
    with col5: work_type = st.selectbox("Primary Employment Domain", options=["Private", "Self-employed", "Govt_job", "children"])
    with col6: residence = st.selectbox("Residence Environment Type", options=["Urban", "Rural"])

    smoking_status = st.selectbox("Smoking Habits Context", options=["never smoked", "formerly smoked", "smokes", "Unknown"])

    # ENCODING MAPS
    gender_map = {"Female": 0, "Male": 1}; married_map = {"No": 0, "Yes": 1}
    work_map = {"Govt_job": 0, "Private": 1, "Self-employed": 2, "children": 3}; residence_map = {"Rural": 0, "Urban": 1}
    smoking_map = {"Unknown": 0, "formerly smoked": 1, "never smoked": 2, "smokes": 3}

    gender_enc = gender_map[gender]; married_enc = married_map[ever_married]
    work_enc = work_map[work_type]; residence_enc = residence_map[residence]; smoking_enc = smoking_map[smoking_status]
    hyper_enc = 1 if hypertension == "Yes" else 0; heart_enc = 1 if heart_disease == "Yes" else 0

    raw_patient_features = [gender_enc, age, hyper_enc, heart_enc, married_enc, work_enc, residence_enc, glucose, bmi, smoking_enc]

    if st.button("🔬 Execute AI Cardiovascular Diagnostics", use_container_width=True):
        try:
            input_array = np.array([raw_patient_features])
            if stroke_scaler is not None:
                if stroke_scaler.n_features_in_ == 10:
                    input_array = stroke_scaler.transform(input_array)
                elif stroke_scaler.n_features_in_ == 3:
                    scaled_nums = stroke_scaler.transform([[age, glucose, bmi]])[0]
                    input_array = np.array([[gender_enc, scaled_nums[0], hyper_enc, heart_enc, married_enc, work_enc, residence_enc, scaled_nums[1], scaled_nums[2], smoking_enc]])

            stroke_risk_prediction = logistic_model.predict(input_array)[0]

            st.markdown("---")
            if stroke_risk_prediction == 1:
                st.markdown("""
                <div style='background-color: #FDEDEC; padding: 25px; border-radius: 12px; border-left: 8px solid #922B21;'>
                    <h2 style='color: #922B21; margin-top: 0;'>⚠️ Evaluation Alert: High Risk Detected</h2>
                    <p style='color: #2C3E50; font-size: 16px;'>The analytical model reports metrics correlated with high-risk classification zones.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # --- THE NEW SMART TARGET CALCULATOR ---
                st.markdown("### 🎯 Your Target Normalization Limits")
                
                # Calculate standard clinical gaps
                target_bmi = 24.9
                target_glucose = 99.0
                
                bmi_gap = max(0.0, bmi - target_bmi)
                glucose_gap = max(0.0, glucose - target_glucose)
                
                st.info(f"""
                💡 **How to return your metric profile back to Normal:**
                *   **BMI Target:** Your current BMI is `{bmi}`. To fall back into the safe/normal target window, you should ideally aim to reduce your BMI by **`{bmi_gap:.1f}`** points to reach the safe limit of **`24.9`**.
                *   **Glucose Target:** Your current glucose is `{glucose} mg/dL`. To hit a traditional normal metabolic limit, you should aim to lower your glucose by **`{glucose_gap:.1f} mg/dL`** to sit under **`99.0 mg/dL`**.
                """)
                
                # HEALTH ADVISORY OUTLINE (Diet & Exercise)
                col_diet, col_exe = st.columns(2)
                with col_diet:
                    st.markdown("""
                    <div style='background-color: #FEF9E7; padding: 20px; border-radius: 10px; border-top: 4px solid #D4AC0D; min-height: 250px;'>
                        <h4 style='color: #7D6608; margin-top:0;'>🥗 Recommended Diet Plan</h4>
                        <ul style='font-size: 14px; color: #2C3E50; padding-left: 15px;'>
                            <li><b>Sodium Reduction:</b> Lower salt intake to stabilize blood pressure.</li>
                            <li><b>DASH Framework:</b> Focus on leafy greens, whole grains, and clean lean proteins.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                with col_exe:
                    st.markdown("""
                    <div style='background-color: #EAF2F8; padding: 20px; border-radius: 10px; border-top: 4px solid #2980B9; min-height: 250px;'>
                        <h4 style='color: #1B4F72; margin-top:0;'>🏃‍♀️ Regulated Exercise Routine</h4>
                        <ul style='font-size: 14px; color: #2C3E50; padding-left: 15px;'>
                            <li><b>LISS Cardio:</b> 30 minutes of brisk walking or steady cycling 5 days a week.</li>
                            <li><b>Avoid Sudden Spikes:</b> Avoid heavy unassisted weight lifting without a coach.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background-color: #EAF2F8; padding: 25px; border-radius: 12px; border-left: 8px solid #1F618D; text-align: center;'>
                    <h2 style='color: #1F618D; margin-top: 0;'>✅ Evaluation Profile: Low / Standard Risk</h2>
                    <p style='color: #2C3E50; font-size: 16px; margin-bottom: 0;'>Your metrics sit inside safe baseline parameters. Keep up the healthy lifestyle!</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"🚨 Diagnostic Pipeline Anomaly: {e}")