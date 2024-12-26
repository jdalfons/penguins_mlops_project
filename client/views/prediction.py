import streamlit as st
import pandas as pd
import joblib
import numpy as np
import requests
from penguin_data import descriptions, measures, facts, images


# Function to display the prediction page
def prediction():
    st.title("🤖 Prediction")
    st.write("Welcome to the prediction page!")


    models = (
        'Logistic Regression',
        'K-Nearest Neighbors',
        'Random Forest',
        'Extra Trees'
    )

    # Select model
    model_choice = st.selectbox(
        "Choose a model",
        models
    )

    # Form to input new data
    with st.form("prediction_form"):
        island = st.selectbox("Island", {"Biscoe": 0, "Dream": 1, "Torgersen": 2})
        culmen_length_mm = st.number_input("Culmen Length (mm)", min_value=0.0)
        culmen_depth_mm = st.number_input("Culmen Depth (mm)", min_value=0.0)
        flipper_length_mm = st.number_input("Flipper Length (mm)", min_value=0.0)
        body_mass_g = st.number_input("Body Mass (g)", min_value=0.0)
        sex = st.selectbox("Sex", {"MALE": 0, "FEMALE": 1})
        save_data = st.checkbox("Save data?", value=False)

        submitted = st.form_submit_button("Predict")

        model_choice = {
            'Logistic Regression': 'logReg', 
            'K-Nearest Neighbors': 'knn',
            'Random Forest': 'rf',
            'Extra Trees': 'et'}[model_choice]
        
        if submitted:
            input_data = {
                "island": island,
                "culmen_length_mm": culmen_length_mm,
                "culmen_depth_mm": culmen_depth_mm,
                "flipper_length_mm": flipper_length_mm,
                "body_mass_g": body_mass_g,
                "sex": sex,
                "model": model_choice,
                "insert": save_data
            }

            try:
                st.write(f"### Input Data:")
                st.write(input_data)    
                response = requests.post("http://server:8000/prediction", json=input_data)
                response.raise_for_status()
                prediction = response.json()
                st.write(f"### Prediction Results:")
                st.write(prediction)
                predicted_species = prediction['prediction']
            except requests.exceptions.RequestException as e:
                st.error(f"Request error: {e}")
                return
            except ValueError as e:
                st.error(f"JSON decode error: {e}")
                return
            except KeyError as e:
                st.error(f"Missing data in response: {e}")
                return

            try:
                st.write(f"### Predicted Species: {predicted_species} (model used: {model_choice})")
                species_key = predicted_species.lower()

                st.write("#### Description:")
                st.write(descriptions[species_key])

                st.write("#### Measurements:")
                st.write(measures[species_key], unsafe_allow_html=True)

                st.write("#### Random Fact:")
                st.write(np.random.choice(facts[species_key]))

                st.image(images[species_key], caption=f"{predicted_species} Penguin", use_container_width=True)
            except KeyError as e:
                st.error(f"Error: Missing data for predicted species '{predicted_species}'. Please check the API response and ensure all necessary data is available.")
