from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

model = joblib.load("./models/linear_model_latest.pkl")

# Input is currently forwarded in its final format.
# Here, the format is changes to the early-version model that is 
# currently being used here.

# Model of each soil layer from the frontend
# The optional parameters are not used in the LLMs current state.
class SoilLayer(BaseModel):
    layerNumber: int
    name: Optional[str] = None
    level: float
    Eoed: float
    phi: Optional[float] = None
    c: Optional[float] = None
    unitWeight: Optional[float] = None

# Input format that is received from the frontend.
class JsonBody(BaseModel):
    width: float
    load: float
    eccentricity: float
    soilLayers: List[SoilLayer] = Field(default_factory=list)

# Format that the LLM requires
class ModelInputData(BaseModel):
    foundationWidth: float
    eccentricity: float
    soils: List[float]

def formatInputData(body: JsonBody) -> ModelInputData:
    foundationWidth = body.width
    eccentricity = body.eccentricity
    soils = []

    number_of_layers = 16
    layer_thickness = 0.25
    surface_level = body.soilLayers[0].level

    for i in range(number_of_layers):
        level = surface_level - i*layer_thickness
        for soilLayer in reversed(body.soilLayers):
            if level <= soilLayer.level:
                Eoed = soilLayer.Eoed
                break # Breaking the inner loop (j-looop)
        soils.append(Eoed)

    return ModelInputData(
        foundationWidth=body.width,
        eccentricity=body.eccentricity,
        soils=soils,
    )


# Serving the api 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev
        "http://127.0.0.1:5173",
        # add your prod origin(s) later, e.g. "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],          # or ["POST", "OPTIONS"]
    allow_headers=["*"],
)

@app.post("/predict")
def predict(body: JsonBody):
    data = formatInputData(body)
    print('data')
    print(data)
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    return float(prediction[0])