from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import os
import joblib

app = FastAPI()

try:
    db = psycopg2.connect(
        host="postgres",
        user="mlops",
        password="mlops",
        dbname="mlops"
    )
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
except psycopg2.Error as err:
    raise HTTPException(status_code=500, detail=f"Database connection error: {err}")


class Data(BaseModel):
    species: str
    island: str
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: int
    sex: str
    model: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all_data/")
async def get_all_data():
    try:
        cursor.execute("SELECT * FROM penguin_data")
        result = cursor.fetchall()
    except psycopg2.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")

    if not result:
        raise HTTPException(status_code=404, detail="No data found in the database")

    return {"data": result}


@app.get("/data_query/")
async def get_data_query(params: dict):
    if not params:
        raise HTTPException(status_code=400, detail="Please provide a query parameter")
    if 'query' not in params:
        raise HTTPException(status_code=400, detail="Please provide a query parameter")

    query = params.get('query')
    try:
        cursor.execute(query)
    except psycopg2.Error as err:
        raise HTTPException(status_code=400, detail=f"Invalid SQL query: {err}")

    result = cursor.fetchall()
    return {"data": result}


@app.get("/data/")
async def get_data(request: Request):
    params = request.query_params

    if not params:
        raise HTTPException(status_code=400, detail="Please provide page and page_size parameters")
    if not all(key in params for key in ('page', 'page_size')):
        raise HTTPException(status_code=400, detail="Please provide page and page_size parameters")

    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 10))

    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Page and page_size must be greater than 0")

    offset = (page - 1) * page_size

    cursor.execute("SELECT * FROM penguin_data LIMIT %s OFFSET %s", (page_size, offset))
    result = cursor.fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="No data found in the database")

    return {"data": result}


@app.post("/prediction/")
async def predict(request: Request):
    response = dict()
    data = await request.json()
    data_dict = data

    # Extract the model type
    model_type = data_dict.pop("model")

    # Extract data from request
    island = data_dict['island']
    culmen_length_mm = data_dict['culmen_length_mm']
    culmen_depth_mm = data_dict['culmen_depth_mm']
    flipper_length_mm = data_dict['flipper_length_mm']
    body_mass_g = data_dict['body_mass_g']
    sex = data_dict['sex']

    # Create new data DataFrame
    new_data = pd.DataFrame({
        'island': [island],
        'culmen_length_mm': [float(culmen_length_mm)],
        'culmen_depth_mm': [float(culmen_depth_mm)],
        'flipper_length_mm': [float(flipper_length_mm)],
        'body_mass_g': [float(body_mass_g)],
        'sex': [sex]
    })

    # Encode categorical variables
    new_data['island'] = new_data['island'].map({'Biscoe': 0, 'Dream': 1, 'Torgersen': 2})
    new_data['sex'] = new_data['sex'].map({'FEMALE': 0, 'MALE': 1})

    # Sample and preprocess existing data
    try:
        cursor.execute("SELECT * FROM penguin_data")
        result = cursor.fetchall()
    except psycopg2.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")

    if not result:
        raise HTTPException(status_code=404, detail="No data found in the database")

    df = pd.DataFrame(result, columns=[
        'species', 'island', 'culmen_length_mm', 'culmen_depth_mm',
        'flipper_length_mm', 'body_mass_g', 'sex'
    ])
    df_sampled = df.groupby('species', group_keys=False).apply(lambda x: x.sample(min(len(x), 100)))
    X = df_sampled.drop(columns=['species'])
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
    scaler = StandardScaler()
    scaler.fit(X)
    new_data_scaled = scaler.transform(new_data)

    # Load models
    try:
        os_path = os.path.join(os.getcwd(), "models")
        models = {
            'logReg': joblib.load(os.path.join(os_path, "LogisticRegression.pkl")),
            'knn': joblib.load(os.path.join(os_path, "KNeighborsRegressor.pkl")),
            'rf': joblib.load(os.path.join(os_path, "RandomForestRegressor.pkl")),
            'et': joblib.load(os.path.join(os_path, "ExtraTreesRegressor.pkl"))
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Model file not found: {e}")

    if model_type not in models:
        return {"error": "Invalid model type"}
    response['model'] = model_type

    model = models[model_type]
    prediction = model.predict(new_data_scaled)
    species_mapping = {0: 'Adelie', 1: 'Chinstrap', 2: 'Gentoo'}
    predicted_species = species_mapping[int(np.round(prediction[0]))]
    
    response['prediction'] = predicted_species
    
    if 'insert' in data_dict and data_dict['insert']:
        try:
            try:
                cursor.execute(
                        "INSERT INTO penguin_data (species, island, culmen_length_mm, culmen_depth_mm, flipper_length_mm, body_mass_g, sex) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (predicted_species, data_dict['island'], data_dict['culmen_length_mm'], data_dict['culmen_depth_mm'], data_dict['flipper_length_mm'], data_dict['body_mass_g'], data_dict['sex'])
                    )
                db.commit()
                response['inserted'] = True
            except psycopg2.Error as err:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Database insert error: {err}")
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database insert error: {err}")
        
    return response