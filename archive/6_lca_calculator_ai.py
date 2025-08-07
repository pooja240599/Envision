import streamlit as st
import PyPDF2
import openai
import matplotlib.pyplot as plt
import os

# --- Set page config ---
st.set_page_config(page_title="LCA GHG Calculator", layout="wide")

# --- Load API key from secrets ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Emission Factors (kg CO₂e per unit) ---
EMISSION_FACTORS = {
    "concrete": 0.15,
    "steel": 1.9,
    "diesel": 2.67,
    "electricity": 0.02,
    "transport": 0.1
}

# --- Helper to extract text from PDF ---
def extract_text_from_pdf(uploaded_pdf):
    reader = PyPDF2.PdfReader(uploaded_pdf)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text.strip()

# --- Helper to extract structured input from PDF text using OpenAI ---
def extract_inputs_with_openai(text):
    prompt = f"""
Extract the following numeric values from the construction document text below. Respond ONLY in JSON format:

- project_area_m2: Total bridge area in square meters
- operational_years: Operational life in years
- baseline_total_emissions: Baseline total GHG emissions (in kg CO2e)
- concrete_kg: Concrete used (in kg)
- steel_kg: Steel used (in kg)
- diesel_liters: Diesel used (in liters)
- electricity_kwh: Electricity consumed (in kWh)
- transport_ton_km: Transport in ton-km

Document:
{text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    import json
    return json.loads(response.choices[0].message.content)

# --- LCA Calculation ---
def calculate_emissions(inputs):
    emissions = {
        material: inputs[material + suffix] * factor
        for material, factor in EMISSION_FACTORS.items()
        for suffix in ["_kg", "_liters", "_kwh", "_ton_km"]
        if material + suffix in inputs
    }

    total_ghg = sum(emissions.values())
    annual_ghg = total_ghg / inputs["operational_years"]
    per_m2_annual_ghg = annual_ghg / inputs["project_area_m2"]

    return total_ghg, annual_ghg, per_m2_annual_ghg, emissions

# --- Envision Classification ---
def classify_emission_reduction(baseline, actual):
    reduction = baseline - actual
    percent = (reduction / baseline) * 100 if baseline else 0
    if percent < 5:
        level = "No Improvement"
    elif percent < 15:
        level = "Improved"
    elif percent < 30:
        level = "Enhanced"
    elif percent < 50:
        level = "Superior"
    else:
        level = "Restorative"
    return percent, level

# --- UI ---
st.title("🌿 LCA GHG Emission Calculator (AI-powered)")
st.markdown("Upload a project PDF and we’ll calculate lifecycle emissions using OpenAI.")

uploaded_pdf = st.file_uploader("📄 Upload Project Description PDF", type="pdf")

if uploaded_pdf:
    with st.spinner("Reading and analyzing document..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        inputs = extract_inputs_with_openai(pdf_text)

    st.subheader("📋 Extracted Project Data")
    st.json(inputs)

    if st.button("✅ Submit & Calculate LCA"):
        total, annual, per_m2, breakdown = calculate_emissions(inputs)
        percent_reduction, level = classify_emission_reduction(inputs["baseline_total_emissions"], total)

        st.subheader("📊 Emission Summary")
        st.metric("Total Emissions (kg CO₂e)", f"{total:,.0f}")
        st.metric("Annual Emissions", f"{annual:,.2f} kg CO₂e/year")
        st.metric("Per m² Annual Emissions", f"{per_m2:.2f} kg CO₂e/m²/year")

        st.subheader("📈 Envision Evaluation")
        st.success(f"Performance Level: **{level}** ({percent_reduction:.1f}% reduction from baseline)")

        # Pie Chart
        st.subheader("📊 Emissions Breakdown")
        fig, ax = plt.subplots()
        ax.pie(breakdown.values(), labels=breakdown.keys(), autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        # Bar Chart
        fig2, ax2 = plt.subplots()
        ax2.bar(breakdown.keys(), breakdown.values(), color="skyblue")
        ax2.set_title("Emissions by Material")
        ax2.set_ylabel("kg CO₂e")
        st.pyplot(fig2)
