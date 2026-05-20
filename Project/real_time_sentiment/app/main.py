from fastapi import FastAPI
from app.schemas import TextRequest
from app.model import predict_sentiment

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict(request: TextRequest):

    result = predict_sentiment(request.text)

    return result