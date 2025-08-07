import streamlit as st
import base64
import os

# --- Page Config ---
st.set_page_config(page_title="Envision Framework", layout="wide")

# --- Page Header ---
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1506765515384-028b60a970df?auto=format&fit=crop&w=1470&q=80");
            background-size: cover;
            background-attachment: fixed;
        }
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: white;
            margin-top: 2rem;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.6);
        }
        .sub-text {
            text-align: center;
            font-size: 1.2rem;
            color: #f0f0f0;
            margin-bottom: 3rem;
        }
        .credit-card {
            background: rgba(197, 197, 227, 0.9);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        }
        .credit-icon {
            width: 120px;
            height: 120px;
            margin-bottom: 1rem;
        }
        .credit-label {
            font-size: 1.1rem;
            font-weight: bold;
            color: #1f2937;
            margin-top: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 Envision Sustainability Framework</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Select a category to begin your project evaluation.</div>', unsafe_allow_html=True)

# --- Define Pages and Icons ---
CREDITS = [
    ("Quality of Life", "pages/1_Quality_of_Life.py", "images/quality.png"),
    ("Leadership", "pages/2_Leadership.py", "images/leadership.png"),
    ("Resource Allocation", "pages/3_Resource_Allocation.py", "images/resource.png"),
    ("Natural World", "pages/4_Natural_World.py", "images/natural.png"),
    ("Climate and Resilience", "pages/5_Climate_and_Resilience.py", "images/climate.png"),
]

# --- 2-Column Layout with Icons and Navigation ---
col1, col2 = st.columns(2)

for i, (label, path, icon_path) in enumerate(CREDITS):
    column = col1 if i % 2 == 0 else col2

    with column:
        with open(icon_path, "rb") as img_file:
            encoded_icon = base64.b64encode(img_file.read()).decode()

        st.markdown(f"""
            <div class="credit-card">
                <img class="credit-icon" src="data:image/png;base64,{encoded_icon}" />
                <div class="credit-label">{label}</div>
            </div>
        """, unsafe_allow_html=True)
        st.page_link(path, label="Open", icon="➡️")
