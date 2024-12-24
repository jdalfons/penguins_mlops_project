import pandas as pd
import requests
import joblib
import mlflow
import mlflow.sklearn
import os
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error
from dotenv import load_dotenv

load_dotenv()
mlflow.set_tracking_uri(os.getenv("MLOPS_TRACKING_URI"))
mlflow.set_experiment("penguins")

response = requests.get(os.getenv("PENGUINS_API_URL"))
response.raise_for_status()
data = response.json()
data = pd.DataFrame(
    data['data'],
    columns=[
        "species", "island", "culmen_length_mm", 
        "culmen_depth_mm", "flipper_length_mm", 
        "body_mass_g", "sex"
    ]
)
data = data.dropna()
encoder = LabelEncoder()

for col in ['species', 'island', 'sex']:
    data[col] = encoder.fit_transform(data[col])
X, y = data.drop('species', axis=1), data['species']
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
models = {
    "LogisticRegression": LogisticRegression(),
    "KNeighborsRegressor": KNeighborsRegressor(n_neighbors=3),
    "RandomForestRegressor": RandomForestRegressor(),
    "ExtraTreesRegressor": ExtraTreesRegressor()
}
# Create models directory if it doesn't exist
os.makedirs('./models', exist_ok=True)

# Train and log models
# Train and log models
for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mlflow.log_metric("mse", mse)
        input_example = X_test[:5]
        mlflow.sklearn.log_model(model, model_name, input_example=input_example)
        joblib.dump(model, f'./models/{model_name}.pkl')

print("Models trained and logged successfully.")