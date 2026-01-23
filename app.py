from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np


# Load trained model (downloaded from CI artifacts)
with open("model.pkl", "rb") as f:
    model = joblib.load(f)

app = FastAPI(title="Wine Quality Inference API")

class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.post("/predict")
def predict_wine_quality(data: WineInput):
    features = np.array([[ 
        data.fixed_acidity,
        data.volatile_acidity,
        data.citric_acid,
        data.residual_sugar,
        data.chlorides,
        data.free_sulfur_dioxide,
        data.total_sulfur_dioxide,
        data.density,
        data.pH,
        data.sulphates,
        data.alcohol
    ]])

    prediction = model.predict(features)[0]

    return {
        "name": "Akhilesh Nekar",         
        "roll_no": "2022BCD0034",          
        "wine_quality": int(round(prediction))
    }
