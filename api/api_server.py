from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

model = joblib.load("./models/linear_model_latest.pkl")

# Define input structure (adjust fields to match your training input)
class InputData(BaseModel):
    foundationWidth: float
    eccentricity: float
    soils: list[float]
    
app = FastAPI()

@app.post("/predict")
def predict(data: InputData):
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    return {"prediction": float(prediction[0])}