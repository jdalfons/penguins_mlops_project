import pandas as pd
import requests
import streamlit as st
from streamlit_option_menu import option_menu

from views.analytics import analytics
from views.about import about
from views.prediction import prediction


def get_data():
    """Fetch data from the server and return a cleaned DataFrame."""
    try:
        response = requests.get("http://server:8000/all_data")
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(
            data['data'],
            columns=[
                "Species", "Island", "Culmen Length (mm)", "Culmen Depth (mm)",
                "Flipper Length (mm)", "Body Mass (g)", "Sex"
            ]
        )
        filtered_data = df.dropna()
        return filtered_data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame(
            columns=[
                "Species", "Island", "Culmen Length (mm)", "Culmen Depth (mm)",
                "Flipper Length (mm)", "Body Mass (g)", "Sex"
            ]
        )

def main():
    df = get_data()

    with st.sidebar:
        selected = option_menu(
            menu_title="Penguins Project",
            options=["About", 'Analytics', 'Prediction'],
            icons=['house', 'bar-chart', 'robot'],
            # menu_icon="cast",
            default_index=0
        )

    if selected == "About":
        about()
    elif selected == "Analytics":
        analytics(df)
    elif selected == "Prediction":
        prediction()

if __name__ == "__main__":
    main()