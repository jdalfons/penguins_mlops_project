# API

This API provides endpoints to make predictions and retrieve all data related to penguins.

## Send Prediction Request

Endpoint: `localhost:8000/prediction/`

### Request
Send a POST request with the following JSON payload to get a prediction:

```json
{
    "island": "Biscoe",
    "culmen_length_mm": 45.2,
    "culmen_depth_mm": 17.3,
    "flipper_length_mm": 210,
    "body_mass_g": 4500,
    "sex": "MALE",
    "model": "logReg"
}
```

### Response
The response will contain the predicted species and the model used:

```json
{
    "prediction": "Gentoo",
    "model": "logReg"
}
```

## Get All Data

Endpoint: `http://localhost:8000/all_data`

### Request
Send a GET request to retrieve all the penguin data.

### Response
The response will contain an array of data entries, each representing a penguin:

```json
{
    "data": [
        [
            "Adelie",
            "Torgersen",
            39.1,
            18.7,
            181.0,
            3750,
            "MALE"
        ],
        [
            "Adelie",
            "Torgersen",
            39.5,
            17.4,
            186.0,
            3800,
            "FEMALE"
        ] 
        ...
    ]
}
```
