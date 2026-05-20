from fastapi import FastAPI
from app.schemas import TextRequest
from app.model import predict_sentiment

import logging
import pandas as pd
import os

logging.basicConfig(
    filename="logs/predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

app = FastAPI()

CSV_FILE = "monitoring/predictions.csv"

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict(request: TextRequest):

    result = predict_sentiment(request.text)

    label = result[0]["label"]
    score = result[0]["score"]

    log_message = (
        f'TEXT="{request.text}" | '
        f'PREDICTION="{label}" | '
        f'SCORE={score}'
    )

    logging.info(log_message)

    new_data = pd.DataFrame([
        {
            "text": request.text,
            "label": label,
            "score": score
        }
    ])

    if os.path.exists(CSV_FILE):
        new_data.to_csv(
            CSV_FILE,
            mode="a",
            header=False,
            index=False
        )

    return result