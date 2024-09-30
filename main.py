from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import joblib
import pandas as pd

app = FastAPI()

sentiment_analyzer = pipeline("sentiment-analysis")

class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

@app.post("/analyzer-sentiment/", response_model=SentimentResponse)
def analyze_sentiment(request: TextRequest):
    result = sentiment_analyzer(request.text)[0]
    sentiment = result['label']
    confidence = result['score']

    return SentimentResponse(sentiment=sentiment, confidence=confidence)


loaded_pipeline = joblib.load("trained_pipeline.pkl")


class IrisDataRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionResponse(BaseModel):
    prediction: list



@app.post("/predict", response_model=PredictionResponse)
def predict_iris(data: IrisDataRequest):
    new_data = pd.DataFrame({
        'sepal length (cm)': [data.sepal_length],
        'sepal width (cm)': [data.sepal_width],
        'petal length (cm)': [data.petal_length],
        'petal width (cm)': [data.petal_width]
    })
    predictions = loaded_pipeline.predict(new_data)
    
    return PredictionResponse(prediction=predictions.tolist())