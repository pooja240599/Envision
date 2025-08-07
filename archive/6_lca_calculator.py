import streamlit as st
import matplotlib.pyplot as plt
import PyPDF2
import re

st.set_page_config(page_title="LCA Calculator", layout="wide")

# --- Emission Factors (kg CO2e per unit) ---
EMISSION_FACTORS = {
    "concrete": 0.15,
    "steel": 1.9,
    "diesel": 2.67,
    "electricity": 0.02,
    "transport": 0.1
}

# --- PDF Extraction Function ---
def extract_inputs_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    def extract(pattern, default):
        match = re.search(pattern, text, re.IGNORECASE)
        try:
            return float(match.group(1).replace(",", "")) if match else default
        except:
            return default

    return {
        "project_area_m2": extract(r"Total Bridge Area\s*[:=]\s*([\d,\.]+)", 10000),
        "operational_years": extract(r"Operational Life\s*[:=]\s*([\d,\.]+)", 100),
        "baseline_total_emissions": extract(r"Baseline Total GHG\s*[:=]\s*([\d,\.]+)", 1_000_000),
        "concrete_kg": extract(r"Concrete Used\s*[:=]\s*([\d,\.]+)\s*kg", 1_000_000),
        "steel_kg": extract(r"Steel Used\s*[:=]\s*([\d,\.]+)\s*kg", 500_000),
        "diesel_liters": extract(r"Diesel Consumption\s*[:=]\s*([\d,\.]+)", 100_000),
        "electricity_kwh": extract(r"Electricity Consumption\s*[:=]\s*([\d,\.]+)", 50_000),
        "transport_ton_km": extract(r"Transport\s*\(Ton[-–]Km\)\s*[:=]\s*([\d,\.]+)", 200_000)
    }

# --- Emission Calculations ---
def calculate_emissions(inputs):
    total = {
        k: inputs[k + "_kg"] * EMISSION_FACTORS[k] if k in ["concrete", "steel"]
        else inputs[k + ("_liters" if k == "diesel" else "_kwh" if k == "electricity" else "_ton_km")] * EMISSION_FACTORS[k]
        for k in EMISSION_FACTORS
    }
    total_ghg = sum(total.values())
    annual_ghg = total_ghg / inputs["operational_years"]
    per_m2_annual_ghg = annual_ghg / inputs["project_area_m2"]
    return total_ghg, annual_ghg, per_m2_annual_ghg, total

# --- Classification ---
def classify_emission_reduction(baseline, project):
    reduction = baseline - project
    percent_reduction = (reduction / baseline) * 100 if baseline > 0 else 0
    if percent_reduction < 5:
        level = "No Improvement"
    elif percent_reduction < 15:
        level = "Improved"
    elif percent_reduction < 30:
        level = "Enhanced"
    elif percent_reduction < 50:
        level = "Superior"
    else:
        level = "Restorative"
    return percent_reduction, level

# --- UI Layout ---
st.title("CR1.2 Reduce Greenhouse Gas Emissions")
st.markdown("Estimate lifecycle GHG emissions and classify per Envision standards")

st.info("""
**Units Explained:**
- **kg CO₂e**: Kilograms of carbon dioxide equivalent – a standard unit for measuring carbon footprints.
- **kg CO₂e/year**: Total emissions released annually.
- **kg CO₂e/m²/year**: Emissions per square meter per year.
""")

# --- Upload PDF ---
uploaded_file = st.file_uploader("📄 Upload Your Project PDF", type=["pdf"])

if uploaded_file:
    inputs = extract_inputs_from_pdf(uploaded_file)
    st.subheader("📋 Extracted Project Data")
    st.json(inputs)

    if st.button("✅ Submit & Calculate"):
        total_ghg, annual_ghg, per_m2_annual_ghg, breakdown = calculate_emissions(inputs)
        percent_reduction, envision_level = classify_emission_reduction(inputs["baseline_total_emissions"], total_ghg)

        # Save results in session
        st.session_state.lca_done = True
        st.session_state.cr1_2_status = envision_level
        st.session_state.cr1_2_points = {
            "No Improvement": -5,
            "Improved": 5,
            "Enhanced": 10,
            "Superior": 15,
            "Restorative": 20
        }.get(envision_level, 0)
        
        # Results
        st.subheader("📊 Emission Summary")
        st.metric("Total GHG Emissions (100 years)", f"{total_ghg:,.2f} kg CO₂e")
        st.metric("Annual Emissions", f"{annual_ghg:,.2f} kg CO₂e/year")
        st.metric("Annual Emissions per m²", f"{per_m2_annual_ghg:.2f} kg CO₂e/m²/year")

        st.subheader("📈 Envision Evaluation")
        st.write(f"**Reduction from Baseline:** {percent_reduction:.1f}%")
        st.success(f"Performance Level: {envision_level}")

        # Pie chart
        st.subheader("📊 Emissions Breakdown by Category")
        fig, ax = plt.subplots()
        ax.pie(breakdown.values(), labels=breakdown.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        # Bar chart
        fig2, ax2 = plt.subplots()
        ax2.bar(breakdown.keys(), breakdown.values(), color='skyblue')
        ax2.set_ylabel("Emissions (kg CO₂e)")
        ax2.set_title("Emissions by Material/Activity")
        st.pyplot(fig2)
else:
    st.warning("Please upload a PDF to proceed.")

