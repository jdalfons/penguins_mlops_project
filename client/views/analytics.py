import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# Function to display the analytics page
def analytics(df):
    st.title("🐧 Palmer penguins Analytics")
    st.write("### Data Exploration")

    def display_sort_options(df):
        top_menu = st.columns(3)
        with top_menu[0]:
            sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=True, index=1)
        if sort == "Yes":
            with top_menu[1]:
                sort_field = st.selectbox("Sort By", options=df.columns)
            with top_menu[2]:
                sort_direction = st.radio(
                    "Direction", options=["⬆️", "⬇️"], horizontal=True
                )
            df = df.sort_values(
                by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
            )
        return df

    def display_pagination(df):
        pagination = st.container()
        bottom_menu = st.columns((4, 1, 1))
        with bottom_menu[2]:
            batch_size = st.selectbox("Page Size", options=[10, 25, 50, 100])
        with bottom_menu[1]:
            total_pages = max(1, int(len(df) / batch_size))
            current_page = st.number_input(
                "Page", min_value=1, max_value=total_pages, step=1
            )
        with bottom_menu[0]:
            st.markdown(f"Page **{current_page}** of **{total_pages}** ")

        start_idx = (current_page - 1) * batch_size
        end_idx = start_idx + batch_size
        st.write(df.iloc[start_idx:end_idx])
        return df.iloc[start_idx:end_idx]

    def plot_bar(data, var, n=5):
        fig = px.bar(
            data, x=var, y=data[var].value_counts().values, color=var,
            title=f'Penguin - {var}', labels={var: var, 'y': 'Frequency'}
        )
        fig.update_layout(xaxis_title=var, yaxis_title='Frequency', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    def box_plot_method(data, variable, group='Species'):
        plt.figure()
        sns.boxplot(x=group, y=variable, data=data, hue=group, palette="Set2", legend=False)
        plt.title(f'Boxplot of {variable} by {group}')
        if plt.gca().get_legend_handles_labels()[1]:
            plt.legend().set_visible(False)
        return plt

    def display_plots(df):
        categorical_vars = ['Species', 'Island', 'Sex']
        numerical_vars = ['Culmen Length (mm)', 'Culmen Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)']
        selected_var = st.selectbox("Select variable", categorical_vars + numerical_vars)
        if selected_var in numerical_vars:
            fig = px.box(df, x='Species', y=selected_var, color='Species', title=f'Boxplot of {selected_var} by Species')
        else:
            fig = px.histogram(df, x=selected_var, color=selected_var, title=f'Frequency of {selected_var}', barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    def display_facet_grid(df):
        x_var = st.selectbox("Select X variable", ['Culmen Length (mm)', 'Culmen Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)'])
        y_var = st.selectbox("Select Y variable", ['Culmen Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)', 'Culmen Length (mm)'])
        if x_var == y_var:
            st.warning("X and Y variables cannot be the same. Please select different variables.")
            return
        fig = px.scatter(df, x=x_var, y=y_var, color='Species', symbol='Species')
        st.plotly_chart(fig, key="penguins", use_container_width=True)

    st.write("""
    In the following you'll perform analytics on the Palmer Penguins dataset and display various visualizations.
    Parameters:
    This data contains measurements for three different species of penguins: Adelie, Chinstrap, and Gentoo.
    The dataset includes the following features:
    - **species**: The species of the penguin (Adelie, Chinstrap, Gentoo)
    - **island**: The island in the Palmer Archipelago where the penguin was observed (Biscoe, Dream, Torgersen)
    - **bill_length_mm**: The length of the penguin's bill (in millimeters)
    - **bill_depth_mm**: The depth of the penguin's bill (in millimeters)
    - **Flipper Length (mm)**: The length of the penguin's flipper (in millimeters)
    - **Body Mass (g)**: The body mass of the penguin (in grams)
    - **Sex**: The sex of the penguin (male, female)
    - **year**: The year in which the observation was made (2007, 2008, 2009)
    """)
    df_display = display_sort_options(df)
    display_pagination(df_display)

    st.write("### Data Visualization")
    st.write("The following plots display the distribution of both categorical and numerical variables. For each type of variable, we have selected the graph type that best represents its distribution.")
    display_plots(df)

    st.write("### Facet Grid")
    st.write("The following plot displays the relationship between two numerical variables, with the data points colored by species.")
    st.write("Select the variables to plot:")
    display_facet_grid(df)
