from fastapi import FastAPI, Header, HTTPException, Request
from app.schemas import TextRequest
from app.model import predict_sentiment

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from dotenv import load_dotenv

import logging
import pandas as pd
import os
import time

load_dotenv()

API_KEY = os.getenv("API_KEY")

logging.basicConfig(
    filename="logs/predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda r, e: HTTPException(
    status_code=429,
    detail="Rate limit exceeded"
))
app.add_middleware(SlowAPIMiddleware)

CSV_FILE = "monitoring/predictions.csv"

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
@limiter.limit("5/minute")
def predict(
    request: Request,
    body: TextRequest,
    x_api_key: str = Header(None)
):

    start_time = time.time()

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    result = predict_sentiment(body.text)

    label = result[0]["label"]
    score = result[0]["score"]

    response_time = round(time.time() - start_time, 4)

    log_message = (
        f'TEXT="{body.text}" | '
        f'PREDICTION="{label}" | '
        f'SCORE={score} | '
        f'RESPONSE_TIME={response_time}s'
    )

    logging.info(log_message)

    new_data = pd.DataFrame([
        {
            "text": body.text,
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

    return {
        "prediction": result,
        "response_time": response_time
    }


'''
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


----    


'''