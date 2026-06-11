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
    st.markdown("<h3 style='text-align: center; color: #595959; font-weight: normal;'>Advanced linear clinical modeling with personalized lifestyle guidance.</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Provide your physiological indicators on the next screen to calculate your dynamic stroke risk score and health plan.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("GO", type="primary", use_container_width=True):
        switch_page('app_interface')
        st.rerun()

# ==========================================
# PAGE 2: MAIN PREDICTOR APP INTERFACE
# ==========================================
elif st.session_state.current_page == 'app_interface':
    st.markdown("<h2 style='color: #1F497D; margin-bottom: 0;'>📊 Patient Health Indicators</h2>", unsafe_allow_html=True)
    st.write("Adjust the clinical variables below. The calibrated scoring engine updates the risk profile instantly.")
    
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
    stroke_probability = 5.0
    
    if age > 30:
        stroke_probability += (age - 30) * 0.5
    if avg_glucose > 90:
        stroke_probability += (avg_glucose - 90) * 0.15
    if bmi > 22.0:
        stroke_probability += (bmi - 22.0) * 0.6
        
    if hypertension == "Yes":
        stroke_probability += 15.0
    if heart_disease == "Yes":
        stroke_probability += 20.0
        
    if smoking_status == "Formerly Smoked":
        stroke_probability += 5.0
    elif smoking_status == "Regular Smoker":
        stroke_probability += 12.0
        
    stroke_probability = max(0.0, min(100.0, stroke_probability))
    
    # ==========================================
    # 4. CONDITIONAL GUIDANCE ENGINE DATA
    # ==========================================
    if stroke_probability < 25.0:
        bg_color = "#E2EFDA"      # Soft Green
        text_color = "#375623"    # Dark Green
        border_color = "#A9D08E"
        status_text = "🟢 Low Stroke Risk Profile"
        
        # Recommendations
        diet_title = "🥗 Preventive Nutrition Plan"
        diet_desc = "Maintain a clean **Mediterranean-style eating pattern**. Focus on healthy fats like extra virgin olive oil and nuts, lean proteins (poultry, fish), and plenty of vibrant fruits and vegetable fiber to keep blood vessels clear."
        
        exec_title = "🏃‍♂️ Maintenance Fitness Plan"
        exec_desc = "Aim for **150 minutes of moderate aerobic exercise** per week. Brisk walking, cycling, or swimming for 30 minutes, 5 days a week, combined with light resistance training, will keep your cardiovascular system in peak condition."

    elif stroke_probability < 55.0:
        bg_color = "#FFF2CC"      # Soft Yellow
        text_color = "#7F6000"    # Dark Gold
        border_color = "#FFD966"
        status_text = "🟡 Moderate Stroke Risk Profile"
        
        # Recommendations
        diet_title = "🥑 DASH Diet Interventions"
        diet_desc = "Transition to the **DASH Diet framework**. Actively reduce sodium intake to under **2,300 mg per day**. Increase your potassium intake with leafy greens and bananas to actively help relax blood vessel walls."
        
        exec_title = "🚴‍♂️ Active Cardio Conditioning"
        exec_desc = "Focus on **consistent cardiovascular workouts**. Dedicate 30 to 45 minutes to active jogging, brisk cycling, or swimming 4 to 5 days a week. Regular aerobic movement is crucial here to improve arterial elasticity."

    else:
        bg_color = "#FCE4D6"      # Soft Red
        text_color = "#C65911"    # Dark Red
        border_color = "#F4B183"
        status_text = "🔴 High Stroke Risk Profile"
        
        # Recommendations
        diet_title = "⚠️ Strict Cardioprotective Diet"
        diet_desc = "Implement a **strict low-sodium protocol** (< 1,500 mg/day). Completely eliminate trans fats, processed meats, and refined sugars. Focus heavily on foods rich in Omega-3 fatty acids and soluble fiber to manage arterial plaque."
        
        exec_title = "🚶‍♂️ Controlled Low-Impact Mobility"
        exec_desc = "Prioritize safety. Focus on **low-impact movements** like therapeutic pacing, slow walking, and mobility exercises. Avoid sudden, heavy straining or high-intensity lifting. *Note: Consult your physician before initiating new routines.*"

    # ==========================================
    # 5. RISK OUTPUT CARD DISPLAY
    # ==========================================
    st.subheader("🔮 2. Dynamic Stroke Risk Evaluation")
    
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 35px; border-radius: 15px; text-align: center; border: 2px solid {border_color}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); margin-bottom: 25px;">
        <p style="font-size: 13px; font-weight: bold; color: #595959; letter-spacing: 1.5px; margin: 0; padding-bottom: 5px;">PROBABILITY ASSESSMENT</p>
        <h1 style="font-size: 70px; margin: 5px 0; color: {text_color}; font-weight: 900; line-height: 1;">{stroke_probability:.1f}<span style="font-size: 30px; font-weight: normal; color: #595959;">%</span></h1>
        <p style="font-size: 20px; font-weight: bold; color: {text_color}; margin: 10px 0 0 0;">{status_text}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # 6. DYNAMIC LIFESTYLE PLAN DISPLAY
    # ==========================================
    st.subheader("📋 3. Personalized Lifestyle Guidance")
    
    # Create side-by-side advice boxes using columns
    plan_col1, plan_col2 = st.columns(2)
    
    with plan_col1:
        st.markdown(f"""
        <div style="background-color: #F8F9FA; padding: 22px; border-radius: 12px; border-left: 5px solid #1F497D; min-height: 200px; box-shadow: 0px 3px 8px rgba(0,0,0,0.02);">
            <h4 style="color: #1F497D; margin-top: 0; margin-bottom: 10px;">{diet_title}</h4>
            <p style="font-size: 14px; color: #404040; line-height: 1.5; margin: 0;">{diet_desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with plan_col2:
        st.markdown(f"""
        <div style="background-color: #F8F9FA; padding: 22px; border-radius: 12px; border-left: 5px solid #008080; min-height: 200px; box-shadow: 0px 3px 8px rgba(0,0,0,0.02);">
            <h4 style="color: #008080; margin-top: 0; margin-bottom: 10px;">{exec_title}</h4>
            <p style="font-size: 14px; color: #404040; line-height: 1.5; margin: 0;">{exec_desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Return button
    if st.button("⬅️ Return to Welcome Page", use_container_width=True):
        switch_page('welcome')
        st.rerun()