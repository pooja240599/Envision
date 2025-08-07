import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Envision Credits", layout="wide")

# --- Define Main Credits and Subcredits ---
CREDITS = {
    "Quality of Life": [
        "QL1.1 Improve Community Quality of Life",
        "QL1.2 Enhance Public Health & Safety",
        "QL1.3 Improve Construction Safety",
        "QL1.4 Minimize Noise & Vibration",
        "QL1.5 Minimize Light Pollution",
        "QL1.6 Minimize Construction Impacts",
        "QL2.1 Improve Community Mobility & Access",
        "QL2.2 Encourage Sustainable Transportation",
        "QL2.3 Improve Access & Wayfinding",
        "QL3.1 Advance Equity & Social Justice",
        "QL3.2 Preserve Historic & Cultural Resources",
        "QL3.3 Enhance Views & Local Character",
        "QL3.4 Enhance Public Space & Amenities",
        "QL0.0 Innovate or Exceed Credit Requirements",
    ],
    "Climate and Resilience": [
        "CR1.1 Reduce Net Embodied Carbon",
        "CR1.2 Reduce Greenhouse Gas Emissions",
        "CR1.3 Reduce Air Pollutant Emissions",
        "CR2.1 Avoid Unsuitable Development",
        "CR2.2 Assess Climate Change Vulnerability",
        "CR2.3 Evaluate Risk and Resilience",
        "CR2.4 Establish Resilience Goals and Strategies",
        "CR2.5 Maximize Resilience",
        "CR2.6 Improve Infrastructure Integration",
        "CR0.0 Innovate or Exceed Credit Requirements"
    ],
    # Add other categories similarly...
}

# --- Session State to Navigate ---
if "selected_credit" not in st.session_state:
    st.session_state.selected_credit = None

if "selected_subcredit" not in st.session_state:
    st.session_state.selected_subcredit = None

# --- Render First Page: Main Credit Buttons ---
if not st.session_state.selected_credit:
    st.title("Envision Framework")
    st.subheader("Select a Credit Category")

    cols = st.columns(3)
    index = 0
    for credit in CREDITS:
        with cols[index % 3]:
            if st.button(credit, use_container_width=True):
                st.session_state.selected_credit = credit
        index += 1

# --- Render Second Page: Subcredit Buttons ---
elif not st.session_state.selected_subcredit:
    st.title(f"Subcredits - {st.session_state.selected_credit}")
    st.subheader("Select a Subcredit")

    subcredits = CREDITS[st.session_state.selected_credit]
    for subcredit in subcredits:
        if st.button(subcredit, key=subcredit):
            st.session_state.selected_subcredit = subcredit

# --- Render Final Page: LCA Calculator ---
else:
    if st.session_state.selected_subcredit == "CR1.2 Reduce Greenhouse Gas Emissions":
        switch_page("lca_calculator")  # This assumes you have a separate page named 'lca_calculator.py'
    else:
        st.title(st.session_state.selected_subcredit)
        st.info("This section is under development.")
        if st.button("⬅ Back to Subcredits"):
            st.session_state.selected_subcredit = None
