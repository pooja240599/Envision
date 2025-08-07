import streamlit as st
import pandas as pd

st.set_page_config(page_title="Climate & Resilience", layout="wide")
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?auto=format&fit=crop&w=1470&q=80");
            background-size: cover;
            background-attachment: fixed;
            }
    </style>
        """, unsafe_allow_html=True)
# --- Header ---
st.title("🌍 Climate and Resilience")
st.markdown("Select a sub-credit below to begin evaluation.")

# --- Subcredits Display ---
subcredits = {
    "CR1.1": "Reduce Net Embodied Carbon",
    "CR1.2": "Reduce Greenhouse Gas Emissions",
    "CR1.3": "Reduce Air Pollutant Emissions",
    "CR2.1": "Avoid Unsuitable Development",
    "CR2.2": "Assess Climate Change Vulnerability",
    "CR2.3": "Evaluate Risk and Resilience",
    "CR2.4": "Establish Resilience Goals and Strategies",
    "CR2.5": "Maximize Resilience",
    "CR2.6": "Improve Infrastructure Integration"
}

st.markdown("### 📌 Sub-Credit Categories")
for key, val in subcredits.items():
    if st.button(f"{key}: {val}"):
        if key == "CR1.2":
            st.switch_page("pages/6_lca_calculator_ai2.py")  # Navigate to LCA calculator

# --- Initialize or update session state for assessment ---
if "assessment_table" not in st.session_state:
    st.session_state.assessment_table = pd.DataFrame({
        "Credit": list(subcredits.keys()),
        "Subcredit": list(subcredits.values()),
        "Status": ["Not Assessed"] * 9,
        "Points": ["-"] * 9,
        "Max Points": [20, 26, 18, 16, 20, 26, 20, 26, 18]
    })

# --- Mock: Update CR1.2 if LCA is done (you can link this dynamically with app logic) ---
#if "lca_done" in st.session_state and st.session_state.lca_done:
#    cr12_idx = st.session_state.assessment_table[st.session_state.assessment_table["Credit"] == "CR1.2"].index[0]
#    st.session_state.assessment_table.loc[cr12_idx, "Status"] = "Enhanced"
 #   st.session_state.assessment_table.loc[cr12_idx, "Points"] = 15  # Example points
    
if st.session_state.get("lca_done", False):
    idx = st.session_state.assessment_table[st.session_state.assessment_table["Credit"] == "CR1.2"].index[0]
    st.session_state.assessment_table.loc[idx, "Status"] = st.session_state.get("cr1_2_status", "Enhanced")
    st.session_state.assessment_table.loc[idx, "Points"] = st.session_state.get("cr1_2_points", 10)

# --- Show Table Toggle ---
if st.checkbox("📋 Show Assessment Checklist Table",key="show_assessment_table"):
    def style_assessment_table(df):
        df = df.copy()

        # Ensure unique index to avoid Styler.apply errors
        df.reset_index(drop=True, inplace=True)

        # Style cells based on Status and Points
        def style_cells(val):
            if isinstance(val, int):
                if val <= 5:
                    return "background-color: #f44336; color: white; font-weight: bold; text-align: center"
                else:
                    return "background-color: #4CAF50; color: white; font-weight: bold; text-align: center"
            elif isinstance(val, str):
                if val.lower() in ["no improvement", "improved"]:
                    return "background-color: #e57373; color: white; font-weight: bold; text-align: center"
                elif val.lower() in ["enhanced", "superior", "restorative"]:
                    return "background-color: #81C784; color: white; font-weight: bold; text-align: center"
            return "text-align: center"

        styled = df.style.applymap(style_cells, subset=["Status", "Points"])\
                        .set_table_styles([
                            {'selector': 'th',
                            'props': [('background-color', '#1976D2'),
                                    ('color', 'white'),
                                    ('font-size', '16px'),
                                    ('text-align', 'center'),
                                    ('padding', '10px'),
                                    ('border-radius', '5px')]},
                            {'selector': 'td',
                            'props': [('text-align', 'center'),
                                    ('padding', '8px'),
                                    ('font-size', '14px')]},
                            {'selector': 'tr:hover td',
                            'props': [('background-color', '#f1f1f1')]}
                        ])

        return styled



    st.markdown("### 📝 Assessment Overview Table")
    styled_table = style_assessment_table(st.session_state.assessment_table)
    st.dataframe(styled_table, use_container_width=True)

