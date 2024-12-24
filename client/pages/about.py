import streamlit as st

# Function to display the about page
def about():
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.title("Palmer Archipelago (Antarctica) penguin")

    with col2:
        st.image(
            "https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/man/figures/logo.png?raw=true"
        )

    st.write("### Introduction")
    st.write(
        """
        palmerpenguins is a dataset for data exploration and visualization,
        providing an alternative to the classic iris dataset. The dataset
        contains information on 344 penguins from 3 different species
        (Adelie, Chinstrap, Gentoo) collected from 3 islands in the Palmer Archipelago,
        Antarctica.
        """
    )

    st.write(
        """
        This application was created to demonstrate the use of different prediction models
        which were verified in the following [kaggle](https://www.kaggle.com/code/halcolo/palmer-penguins-models-training-tutorial)
        notebook.
        """
    )

    st.write("### Source")
    st.write(
        """
        The original project is available on [GitHub](https://github.com/allisonhorst/palmerpenguins/).
        Data were collected and made available by Dr. Kristen Gorman and the Palmer Station, Antarctica LTER,
        a member of the Long Term Ecological Research Network.
        """
    )
    st.image(
        "https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/man/figures/lter_penguins.png?raw=true"
    )