import streamlit as st

# 1. Page Configurations
st.set_page_config(
    page_title="Global Destination Predictor",
    page_icon="✈️",
    layout="centered"
)

# 2. Manage App Navigation via Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

def switch_page(page_name):
    st.session_state.current_page = page_name

# ==========================================
# PAGE 1: WELCOME / LANDING PAGE
# ==========================================
if st.session_state.current_page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #1F497D;'>✈️ Travel Destination Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #595959; font-weight: normal;'>Discover your next perfect getaway powered by predictive analytics.</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Configure your customized profile on the next page to unlock your getaway results.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("GO", type="primary", use_container_width=True):
        switch_page('app_inputs')
        st.rerun()

# ==========================================
# PAGE 2: USER PREFERENCE INPUTS PAGE (ALL DROPDOWNS)
# ==========================================
elif st.session_state.current_page == 'app_inputs':
    st.markdown("<h2 style='color: #1F497D; margin-bottom: 0;'>📊 Configure Your Travel Profile</h2>", unsafe_allow_html=True)
    st.write("Select your choices from the dropdown blocks below. Your inputs will be analyzed on a separate page next.")
    
    st.markdown("---")
    
    # 2-Column Grid for Dropdown Selectors
    col1, col2 = st.columns(2)
    
    with col1:
        chosen_season = st.selectbox("Preferred Season", options=["Summer Vibe", "Winter / Snow", "Spring Blooms", "Autumn Colors"])
        chosen_budget = st.selectbox("Budget Tier", options=["Low (Budget-Friendly)", "Standard (Moderate)", "Luxury (Premium)"])
        chosen_persons = st.selectbox("Number of Persons", options=["1 Person (Solo)", "2 Persons", "3 - 5 Persons", "6+ Persons (Large Group)"])
        
    with col2:
        chosen_type = st.selectbox("Trip Style / Companion", options=["Solo Adventure", "Couples / Romantic Getaway", "Family Holiday", "Friends Trip"])
        chosen_pace = st.selectbox("Trip Pace", options=["Relaxed (Leisure & Unwind)", "Moderate (Sightseeing & Culture)", "Fast-Paced (Heavy Adventure)"])
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Action button to advance to predictions page
    if st.button("🔮 Generate Predictions ➡️", type="primary", use_container_width=True):
        # Save values to session state cache
        st.session_state.user_season = chosen_season
        st.session_state.user_budget = chosen_budget
        st.session_state.user_persons = chosen_persons
        st.session_state.user_type = chosen_type
        st.session_state.user_pace = chosen_pace
        
        switch_page('app_predictions')
        st.rerun()

# ==========================================
# PAGE 3: DEDICATED PREDICTIONS PAGE (SEPARATE)
# ==========================================
elif st.session_state.current_page == 'app_predictions':
    st.markdown("<h2 style='color: #1F497D; margin-bottom: 0;'>🔮 Your Tailored Recommendation Boxes</h2>", unsafe_allow_html=True)
    st.write("Our linear profiling engine evaluated 10 countries against your preferences. Here are your top choices:")
    
    st.markdown("---")
    
    # Fetch parameters safely from state cache
    season = st.session_state.get('user_season', 'Summer Vibe')
    budget_type = st.session_state.get('user_budget', 'Standard (Moderate)')
    trip_type = st.session_state.get('user_type', 'Solo Adventure')
    trip_pace = st.session_state.get('user_pace', 'Moderate (Sightseeing & Culture)')
    
    # Initializing base weights for all 10 destination options
    scores = {
        "The Maldives 🇲🇻": 50, "Paris, France 🇫🇷": 50, "The Swiss Alps 🇨🇭": 50, 
        "Tokyo, Japan 🇯🇵": 50, "Phuket, Thailand 🇹🇭": 50, "Cairo, Egypt 🇪🇬": 50, 
        "Sydney, Australia 🇦🇺": 50, "Reykjavik, Iceland 🇮🇸": 50, "New York City, USA 🇺🇸": 50, 
        "Bali, Indonesia 🇮🇩": 50
    }
    
    # --- Weight Coefficients Layer 1: Season ---
    if season == "Summer Vibe":
        scores["The Maldives 🇲🇻"] += 25; scores["Phuket, Thailand 🇹🇭"] += 25; scores["Bali, Indonesia 🇮🇩"] += 25; scores["Sydney, Australia 🇦🇺"] += 20
    elif season == "Winter / Snow":
        scores["The Swiss Alps 🇨🇭"] += 35; scores["Reykjavik, Iceland 🇮🇸"] += 35; scores["Tokyo, Japan 🇯🇵"] += 15
    elif season == "Spring Blooms":
        scores["Tokyo, Japan 🇯🇵"] += 30; scores["Paris, France 🇫🇷"] += 25; scores["Sydney, Australia 🇦🇺"] += 15
    elif season == "Autumn Colors":
        scores["New York City, USA 🇺🇸"] += 30; scores["Paris, France 🇫🇷"] += 20; scores["Cairo, Egypt 🇪🇬"] += 25

    # --- Weight Coefficients Layer 2: Budget ---
    if budget_type == "Low (Budget-Friendly)":
        scores["Phuket, Thailand 🇹🇭"] += 30; scores["Bali, Indonesia 🇮🇩"] += 30; scores["Cairo, Egypt 🇪🇬"] += 15; scores["The Maldives 🇲🇻"] -= 30; scores["The Swiss Alps 🇨🇭"] -= 30
    elif budget_type == "Standard (Moderate)":
        scores["Tokyo, Japan 🇯🇵"] += 20; scores["Paris, France 🇫🇷"] += 15; scores["Sydney, Australia 🇦🇺"] += 20
    elif budget_type == "Luxury (Premium)":
        scores["The Maldives 🇲🇻"] += 40; scores["The Swiss Alps 🇨🇭"] += 30; scores["New York City, USA 🇺🇸"] += 25; scores["Paris, France 🇫🇷"] += 20

    # --- Weight Coefficients Layer 3: Trip Type ---
    if trip_type == "Solo Adventure":
        scores["Tokyo, Japan 🇯🇵"] += 25; scores["Reykjavik, Iceland 🇮🇸"] += 25; scores["New York City, USA 🇺🇸"] += 20
    elif trip_type == "Couples / Romantic Getaway":
        scores["The Maldives 🇲🇻"] += 35; scores["Paris, France 🇫🇷"] += 30; scores["Bali, Indonesia 🇮🇩"] += 25
    elif trip_type == "Family Holiday":
        scores["Sydney, Australia 🇦🇺"] += 25; scores["The Swiss Alps 🇨🇭"] += 20; scores["Phuket, Thailand 🇹🇭"] += 15
    elif trip_type == "Friends Trip":
        scores["Phuket, Thailand 🇹🇭"] += 25; scores["New York City, USA 🇺🇸"] += 20; scores["Tokyo, Japan 🇯🇵"] += 15

    # --- Weight Coefficients Layer 4: Trip Pace ---
    if trip_pace == "Relaxed (Leisure & Unwind)":
        scores["The Maldives 🇲🇻"] += 30; scores["Bali, Indonesia 🇮🇩"] += 25; scores["Phuket, Thailand 🇹🇭"] += 20
    elif trip_pace == "Moderate (Sightseeing & Culture)":
        scores["Paris, France 🇫🇷"] += 20; scores["Tokyo, Japan 🇯🇵"] += 20; scores["Sydney, Australia 🇦🇺"] += 15; scores["Cairo, Egypt 🇪🇬"] += 20
    elif trip_pace == "Fast-Paced (Heavy Adventure)":
        scores["Reykjavik, Iceland 🇮🇸"] += 30; scores["The Swiss Alps 🇨🇭"] += 25; scores["New York City, USA 🇺🇸"] += 20

    # UI Content & Styling Profiles
    metadata = {
        "The Maldives 🇲🇻": {"bg": "#E2EFDA", "text": "#375623", "border": "#A9D08E", "desc": "An elite tropical getaway optimized for premium luxury, couples, and serene overwater relaxation."},
        "Paris, France 🇫🇷": {"bg": "#D9E1F2", "text": "#1F497D", "border": "#B4C6E7", "desc": "A sophisticated destination packed with iconic arts, world-class historic cafes, and beautiful spring walks."},
        "The Swiss Alps 🇨🇭": {"bg": "#FFF2CC", "text": "#7F6000", "border": "#FFD966", "desc": "Perfect for crisp mountain air, pristine snowy views, active skiing chalets, and family holiday groups."},
        "Tokyo, Japan 🇯🇵": {"bg": "#F5E6FA", "text": "#660066", "border": "#D6A3E4", "desc": "An energetic urban wonderland combining cherry blossoms, neon streets, and amazing food discovery for solos."},
        "Phuket, Thailand 🇹🇭": {"bg": "#E6F4F8", "text": "#006680", "border": "#99D6E6", "desc": "A gorgeous coastal paradise combining warm sunny bays, group activities, and excellent value for your budget."},
        "Cairo, Egypt 🇪🇬": {"bg": "#FCE4D6", "text": "#C65911", "border": "#F4B183", "desc": "Step back in time to explore magnificent ancient pyramids, warm desert climates, and historic bazaar markets."},
        "Sydney, Australia 🇦🇺": {"bg": "#EAF2F8", "text": "#1A5276", "border": "#A9CCE3", "desc": "Ideal for beautiful harbor views, golden surf beaches, coastal family walks, and great summer weather."},
        "Reykjavik, Iceland 🇮🇸": {"bg": "#EBF5FB", "text": "#21618C", "border": "#AED6F1", "desc": "Uncover stunning hot springs, dramatic volcanic geography, and high adventure under the winter Northern Lights."},
        "New York City, USA 🇺🇸": {"bg": "#EAEDED", "text": "#2C3E50", "border": "#CCD1D1", "desc": "The ultimate fast-paced city theater experience featuring Broadway, autumn scaling parks, and premium urban sights."},
        "Bali, Indonesia 🇮🇩": {"bg": "#E8F8F5", "text": "#117A65", "border": "#A3E4D7", "desc": "A peaceful budget-friendly escape filled with scenic cultural temples, tropical surfing, and relaxing beaches."}
    }
    
    # Process sorting
    compiled_destinations = []
    for country, total_score in scores.items():
        item = metadata[country].copy()
        item["name"] = country
        item["score"] = total_score
        compiled_destinations.append(item)
        
    sorted_boxes = sorted(compiled_destinations, key=lambda x: x["score"], reverse=True)
    
    box_1 = sorted_boxes[0]
    box_2 = sorted_boxes[1]
    box_3 = sorted_boxes[2]
    
    # DISPLAY: Box 1 (Primary Highlight Box)
    st.markdown(f"""
    <div style="background-color: {box_1['bg']}; padding: 40px; border-radius: 15px; text-align: center; border: 3px solid {box_1['border']}; box-shadow: 0px 6px 18px rgba(0,0,0,0.08); margin-bottom: 25px;">
        <span style="background-color: {box_1['text']}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; letter-spacing: 1px;">🥇 TOP MATCH PREDICTION</span>
        <h1 style="font-size: 55px; margin: 15px 0 5px 0; color: {box_1['text']}; font-weight: 900; line-height: 1.1;">{box_1['name']}</h1>
        <hr style="border: 0; border-top: 1px solid {box_1['border']}; width: 40%; margin: 12px auto;">
        <p style="font-size: 18px; color: #2C3E50; margin: 5px auto 0 auto; max-width: 520px; font-style: italic; line-height: 1.4;">"{box_1['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # DISPLAY: Alternate Side-by-Side Boxes (Box 2 & Box 3)
    box_col1, box_col2 = st.columns(2)
    
    with box_col1:
        st.markdown(f"""
        <div style="background-color: {box_2['bg']}; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid {box_2['border']}; box-shadow: 0px 4px 12px rgba(0,0,0,0.04); height: 210px;">
            <span style="background-color: {box_2['text']}; color: white; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">🥈 RUNNER UP</span>
            <h3 style="font-size: 24px; margin: 12px 0 8px 0; color: {box_2['text']}; font-weight: 800;">{box_2['name']}</h3>
            <p style="font-size: 14px; color: #4A4A4A; margin: 0; line-height: 1.3;">{box_2['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with box_col2:
        st.markdown(f"""
        <div style="background-color: {box_3['bg']}; padding: 25px; border-radius: 12px; text-align: center; border: 2px solid {box_3['border']}; box-shadow: 0px 4px 12px rgba(0,0,0,0.04); height: 210px;">
            <span style="background-color: {box_3['text']}; color: white; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">🥉 THIRD CHOICE</span>
            <h3 style="font-size: 24px; margin: 12px 0 8px 0; color: {box_3['text']}; font-weight: 800;">{box_3['name']}</h3>
            <p style="font-size: 14px; color: #4A4A4A; margin: 0; line-height: 1.3;">{box_3['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Navigation controls to loop back seamlessly
    back_col1, back_col2 = st.columns(2)
    with back_col1:
        if st.button("⬅️ Change Travel Profile", use_container_width=True):
            switch_page('app_inputs')
            st.rerun()
    with back_col2:
        if st.button("🏠 Exit to Welcome Screen", use_container_width=True):
            switch_page('welcome')
            st.rerun()