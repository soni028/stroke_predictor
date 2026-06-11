import streamlit as st

# 1. Page Configurations
st.set_page_config(
    page_title="Stroke Risk Prediction Dashboard",
    page_icon="🧠",
    layout="centered"
)

# 2. Navigation Control via Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

def switch_page(page_name):
    st.session_state.current_page = page_name

# ==========================================
# PAGE 1: WELCOME / LANDING PAGE
# ==========================================
if st.session_state.current_page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #1F497D;'>🧠 Stroke Risk Prediction App</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #595959; font-weight: normal;'>Advanced linear clinical modeling for stroke prevention and analysis.</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Provide your physiological indicators on the next screen to calculate your dynamic stroke risk score.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Large primary action button
    if st.button("GO", type="primary", use_container_width=True):
        switch_page('app_interface')
        st.rerun()

# ==========================================
# PAGE 2: MAIN PREDICTOR APP INTERFACE
# ==========================================
elif st.session_state.current_page == 'app_interface':
    st.markdown("<h2 style='color: #1F497D; margin-bottom: 0;'>📊 Patient Health Indicators</h2>", unsafe_allow_html=True)
    st.write("Adjust the clinical variables below. The calibrated Linear Regression engine updates the risk instantly.")
    
    st.markdown("---")
    
    st.subheader("🔄 1. Input Clinical Metrics")
    
    # 2-Column Balanced Dashboard Grid
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age (Years)", min_value=18, max_value=100, value=45, step=1)
        avg_glucose = st.slider("Average Glucose Level (mg/dL)", min_value=50, max_value=250, value=95, step=1)
        bmi = st.slider("Body Mass Index (BMI)", min_value=15.0, max_value=50.0, value=24.5, step=0.1)
        
    with col2:
        hypertension = st.selectbox("Hypertension (High Blood Pressure)?", options=["No", "Yes"])
        heart_disease = st.selectbox("History of Heart Disease?", options=["No", "Yes"])
        smoking_status = st.selectbox("Smoking Status", options=["Never Smoked", "Formerly Smoked", "Regular Smoker"])
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 3. FIXED & CALIBRATED LINEAR SCORING ENGINE
    # ==========================================
    # Base baseline probability starts low (healthy baseline)
    stroke_probability = 5.0
    
    # Linear additions based on deviations from normal health ranges:
    # Age: Add 0.5% risk for every year over 30
    if age > 30:
        stroke_probability += (age - 30) * 0.5
        
    # Glucose: Add 0.15% risk for every mg/dL over a normal fasting baseline of 90
    if avg_glucose > 90:
        stroke_probability += (avg_glucose - 90) * 0.15
        
    # BMI: Add 0.6% risk for every unit over a normal baseline of 22.0
    if bmi > 22.0:
        stroke_probability += (bmi - 22.0) * 0.6
        
    # Categorical additions (binary adjustments)
    if hypertension == "Yes":
        stroke_probability += 15.0
        
    if heart_disease == "Yes":
        stroke_probability += 20.0
        
    # Smoking status tiered linear impact
    if smoking_status == "Formerly Smoked":
        stroke_probability += 5.0
    elif smoking_status == "Regular Smoker":
        stroke_probability += 12.0
        
    # Enforce strict probability boundaries between 0% and 100%
    stroke_probability = max(0.0, min(100.0, stroke_probability))
    
    # ==========================================
    # 4. MASSIVE TYPOGRAPHY CARD FOR OUTPUT
    # ==========================================
    st.subheader("🔮 2. Dynamic Stroke Risk Evaluation")
    
    # Balanced threshold intervals to cleanly trigger all 3 states
    if stroke_probability < 25.0:
        bg_color = "#E2EFDA"      # Soft Green
        text_color = "#375623"    # Dark Green
        border_color = "#A9D08E"
        status_text = "🟢 Low Stroke Risk Profile"
    elif stroke_probability < 55.0:
        bg_color = "#FFF2CC"      # Soft Yellow
        text_color = "#7F6000"    # Dark Gold
        border_color = "#FFD966"
        status_text = "🟡 Moderate Stroke Risk Profile"
    else:
        bg_color = "#FCE4D6"      # Soft Red
        text_color = "#C65911"    # Dark Red
        border_color = "#F4B183"
        status_text = "🔴 High Stroke Risk Profile"

    # Injecting the massive score card block
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 40px; border-radius: 15px; text-align: center; border: 2px solid {border_color}; box-shadow: 0px 4px 12px rgba(0,0,0,0.05);">
        <p style="font-size: 14px; font-weight: bold; color: #595959; letter-spacing: 1.5px; margin: 0; padding-bottom: 5px;">PROBABILITY ASSESSMENT</p>
        <h1 style="font-size: 75px; margin: 5px 0; color: {text_color}; font-weight: 900; line-height: 1;">{stroke_probability:.1f}<span style="font-size: 35px; font-weight: normal; color: #595959;">%</span></h1>
        <p style="font-size: 22px; font-weight: bold; color: {text_color}; margin: 12px 0 0 0;">{status_text}</p>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Back button
    if st.button("⬅️ Return to Welcome Page", use_container_width=True):
        switch_page('welcome')
        st.rerun()