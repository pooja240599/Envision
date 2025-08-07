import streamlit as st

st.title("Climate & Resilience Credits")

subcredits = [
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
]

for credit in subcredits:
    if st.button(credit):
        if credit == "CR1.2 Reduce Greenhouse Gas Emissions":
            st.switch_page("pages/6_lca_calculator.py")
