from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from src.ml.feature_engineering import create_features_soil_layers

model = joblib.load("./model.pkl")

# Define input structure (adjust fields to match your training input)
class InputData(BaseModel):
    width: float
    eccentricity: float
    soil_model: str
    soil_modulus: list
    

app = FastAPI()

@app.post("/predict")
def predict(data: InputData):

    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    return {"prediction": float(prediction[0])}