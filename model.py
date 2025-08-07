import spacy
from spacy.training.example import Example
import random

# Step 1: Define training data
training_data = [
    # Project Name
    ("Project Name: East River Smart Bridge", {"entities": [(14, 38, "PROJECT_NAME")]}),
    ("Name of Project - Golden Gate Pathway", {"entities": [(18, 41, "PROJECT_NAME")]}),
    ("Bridge Title: Millennium Link", {"entities": [(15, 31, "PROJECT_NAME")]}),

    # Project Location
    ("Project Location: Boston, MA", {"entities": [(18, 29, "PROJECT_LOCATION")]}),
    ("Location - San Diego, California", {"entities": [(10, 33, "PROJECT_LOCATION")]}),
    ("Site: Denver, CO", {"entities": [(6, 17, "PROJECT_LOCATION")]}),

    # Project Area
    ("Total Bridge Area: 12,500 m²", {"entities": [(20, 26, "PROJECT_AREA"), (27, 29, "UNIT")]}),
    ("Bridge size = 10000 square meters", {"entities": [(13, 18, "PROJECT_AREA"), (19, 33, "UNIT")]}),
    ("Area of Bridge is 8750 sq. m", {"entities": [(20, 24, "PROJECT_AREA"), (25, 31, "UNIT")]}),

    # Operational Years
    ("Operational Life: 100 years", {"entities": [(18, 21, "OPERATIONAL_YEARS"), (22, 27, "UNIT")]}),
    ("Life Expectancy = 80 yrs", {"entities": [(18, 20, "OPERATIONAL_YEARS"), (21, 24, "UNIT")]}),
    ("Service duration: 60 years", {"entities": [(18, 20, "OPERATIONAL_YEARS"), (21, 26, "UNIT")]}),

    # Baseline GHG
    ("Baseline Total GHG: 1,200,000 kg CO₂e", {"entities": [(21, 30, "BASELINE_GHG"), (31, 38, "UNIT")]}),
    ("Baseline Emissions = 950000 kg CO2e", {"entities": [(22, 28, "BASELINE_GHG"), (29, 35, "UNIT")]}),
    ("Total Baseline GHG Emissions: 800000 kgCO₂e", {"entities": [(31, 37, "BASELINE_GHG"), (37, 43, "UNIT")]}),

    # Concrete
    ("Concrete Used: 1,100,000 kg", {"entities": [(0, 13, "MATERIAL"), (15, 24, "QUANTITY"), (25, 27, "UNIT")]}),
    ("Amount of Concrete = 950,000 kilograms", {"entities": [(11, 19, "MATERIAL"), (22, 28, "QUANTITY"), (29, 38, "UNIT")]}),
    ("Concrete Quantity: 500000 kg", {"entities": [(0, 17, "MATERIAL"), (19, 25, "QUANTITY"), (26, 28, "UNIT")]}),
    ("Material: Concrete | Value: 875,000 kg", {"entities": [(10, 18, "MATERIAL"), (28, 34, "QUANTITY"), (35, 37, "UNIT")]}),

    # Steel
    ("Steel Used: 550,000 kg", {"entities": [(0, 10, "MATERIAL"), (12, 19, "QUANTITY"), (20, 22, "UNIT")]}),
    ("Steel Quantity = 660000 kilograms", {"entities": [(0, 14, "MATERIAL"), (17, 23, "QUANTITY"), (24, 33, "UNIT")]}),
    ("Material: Steel | Qty: 450000 kg", {"entities": [(10, 15, "MATERIAL"), (24, 30, "QUANTITY"), (31, 33, "UNIT")]}),
    ("Steel - 700,000 kg", {"entities": [(0, 5, "MATERIAL"), (8, 15, "QUANTITY"), (16, 18, "UNIT")]}),

    # Diesel
    ("Diesel Consumption: 95,000 liters", {"entities": [(0, 19, "MATERIAL"), (21, 27, "QUANTITY"), (28, 34, "UNIT")]}),
    ("Diesel usage = 87000 L", {"entities": [(0, 12, "MATERIAL"), (15, 20, "QUANTITY"), (21, 22, "UNIT")]}),
    ("Fuel: Diesel | Value: 100,000 liters", {"entities": [(6, 12, "MATERIAL"), (22, 28, "QUANTITY"), (29, 35, "UNIT")]}),
    ("Diesel Quantity: 120000 liters", {"entities": [(0, 16, "MATERIAL"), (18, 24, "QUANTITY"), (25, 31, "UNIT")]}),

    # Electricity
    ("Electricity Consumption: 45,000 kWh", {"entities": [(0, 24, "MATERIAL"), (26, 32, "QUANTITY"), (33, 36, "UNIT")]}),
    ("Electricity Used = 67000 kilowatt-hours", {"entities": [(0, 17, "MATERIAL"), (20, 25, "QUANTITY"), (26, 41, "UNIT")]}),
    ("Electricity: 72000 kWh", {"entities": [(0, 11, "MATERIAL"), (13, 18, "QUANTITY"), (19, 22, "UNIT")]}),

    # Transport
    ("Transport (Ton-Km): 210,000 ton-km", {"entities": [(0, 20, "MATERIAL"), (22, 28, "QUANTITY"), (29, 36, "UNIT")]}),
    ("Transport Distance = 125000 ton-km", {"entities": [(0, 17, "MATERIAL"), (20, 26, "QUANTITY"), (27, 34, "UNIT")]}),
    ("Transport: 180000 ton-km", {"entities": [(0, 9, "MATERIAL"), (11, 17, "QUANTITY"), (18, 25, "UNIT")]}),
]


# Step 2: Create blank spaCy model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Step 3: Add labels
for _, annotations in training_data:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Step 4: Train model
optimizer = nlp.begin_training()
for i in range(30):
    random.shuffle(training_data)
    losses = {}
    for text, annotations in training_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example],sgd=optimizer, losses=losses)
    print(f"Iteration {i}: {losses}")

# Step 5: Save model
nlp.to_disk("custom_ner_model")
