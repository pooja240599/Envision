import streamlit as st

# Page setup
st.set_page_config(page_title="Quality of Life", layout="wide")

# Title and description
st.title("Quality of Life")
st.markdown("Explore the Envision subcredits under the **Quality of Life** category.")

# Subcredits list
subcredits = [
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
    "QL0.0 Innovate or Exceed Credit Requirements"
]

# Display subcredits as buttons
st.subheader("Subcredits:")
for credit in subcredits:
    st.button(credit)
