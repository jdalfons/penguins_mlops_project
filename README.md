# Penguin MLOps Project
This project is designed to demonstrate the use of MLOps practices in building and deploying machine learning models. The project focuses on predicting penguin species based on their physical characteristics using the Palmer Penguins dataset.
<table>
<tr>
<td>

This project is designed to demonstrate the use of MLOps practices in building and deploying machine learning models. The project focuses on predicting penguin species based on their physical characteristics using the [Palmer Penguins dataset](https://github.com/allisonhorst/palmerpenguins).

</td>
<td>

<a href="https://github.com/allisonhorst/palmerpenguins">
    <img src="https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/man/figures/logo.png?raw=true" alt="Palmer Penguins Logo" width="700"/>
</a>

</td>
</tr>
</table>

</table>

## Other Version

For cost reasons, the project hosted on GitHub is completely local. However, there is an online version hosted on [HuggingFace](https://huggingface.co/spaces/jdalfonso/penguins/tree/main). This version does not use a database, MLflow, or backend server (API). It only includes the front end using a single Dockerfile, with models hosted within the same repository. It uses pre-cleaned and processed data that is also within the same repository, which can be visited at the following URL:

https://huggingface.co/spaces/jdalfonso/penguins

## API

To know how to use API let's check.

https://github.com/jdalfons/penguins_mlops_project/tree/main/server/README.md 


## Setting Up the Project

To set up the project, you will need to use Docker Compose. Docker Compose allows you to define and manage multi-container Docker applications. Follow the steps below to get started:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/jdalfons/penguins_mlops_project.git
    cd penguin_mlops_project
    ```

2. **Build and start the containers:**
    Use Docker Compose to build and start the containers. Run the following command:
    ```sh
    docker-compose up --build -d
    ```

    This command will build 4 Docker images and start the containers in detached mode.

## Architecture

The architecture of the project is illustrated in the following diagram:

![MLOps Architecture](https://github.com/jdalfons/penguins_mlops_project/raw/main/diagram/docker_mlops.png)


## Running MLflow

MLflow is used to manage the machine learning lifecycle, including experimentation, reproducibility, and model deployment in this case is just to create models and make experimentation about this. Ensure that the environment variables are correctly set in the `.env` file to allow MLflow to function properly.

Create a `.env` file in the mlflow directory and set the necessary environment variables. These variables are crucial for running MLflow. An example `.env` file might look like this:

    ```env
    MLOPS_TRACKING_URI="http://localhost:5001" 
    PENGUINS_API_URL="http://localhost:8000/all_data"
    ```

Once the containers are up and running, you can access the MLflow UI by navigating to `http://localhost:5000` in your web browser.

## Tools

| Tool      | Version  |
|-----------|----------|
| Docker    | Latest   |
| Python    | 3.11     |
| MLflow    | 2.19.0   |
| Streamlit | 1.40.1   |
| FastAPI   | 0.115.5  |

## Conclusion

By following the steps above, you will have a fully functional MLOps environment for developing and deploying machine learning models. Make sure to properly configure your environment variables to ensure smooth operation of MLflow and other services.

Happy coding!

