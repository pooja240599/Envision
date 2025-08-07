import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Envision Framework", layout="wide")

# --- Background Styling ---
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
        }
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1506765515384-028b60a970df?auto=format&fit=crop&w=1470&q=80");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 2rem;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
        }

        .sub-text {
            text-align: center;
            font-size: 1.2rem;
            color: #f3f3f3;
            margin-bottom: 3rem;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
        }

        .stButton > button {
            width: 100%;
            height: 4.5rem;
            font-size: 1.5rem;
            font-weight: bold;
            color: white !important;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            border: none;
            border-radius: 14px;
            margin-top: 1.2rem;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
            transition: all 0.2s ease-in-out;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb, #60a5fa);
            transform: scale(1.05);
            box-shadow: 0px 6px 16px rgba(0,0,0,0.35);
        }
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.markdown('<div class="main-title">🌿 Envision Sustainability Framework</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Select a category to begin your project evaluation.</div>', unsafe_allow_html=True)

# --- Category Buttons ---
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_Quality_of_Life.py", label="Quality of Life", icon="🌍")
    st.page_link("pages/2_Leadership.py", label="Leadership", icon="🧭")
    st.page_link("pages/3_Resource_Allocation.py", label="Resource Allocation", icon="🔋")

with col2:
    st.page_link("pages/4_Natural_World.py", label="Natural World", icon="🦋")
    st.page_link("pages/5_Climate_and_Resilience.py", label="Climate Resilience", icon="🔥")
