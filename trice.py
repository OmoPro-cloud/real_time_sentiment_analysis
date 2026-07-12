from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
import random
import time

app = FastAPI()

#metrics
REQUEST_COUNTER = Counter("api_request_total", "total API requests")
PREDICTION_COUNTER = Counter("model_predictions_total", "Total number of predictions")
REQUEST_LATENCY_HISTOGRAM = Histogram("api_latency_seconds", "request latency in seconds")
CONFIDENCE_HISTOGRAM = Histogram("model_confidence_score", "Confidence score of predictions", buckets=[0.5, 0.7, 0.9, 1.0])

#instrumentator automatically tracks request count, latency, error and /metrics endpoint
instrumentation = Instrumentator().instrument(app).expose(app)

#setup /predict endpoint and model
@app.get("/predict")
def predict(model_version: str = "v1"):
    start_time = time.time() #record start-time for latency measurment

    #simulate a prediction with random confidence score
    classes = ["cat", "dog", "mouse"]
    prediction = random.choice(classes)
    confidence = random.uniform(0.5, 1.0)

    #Increment metrics
    REQUEST_COUNTER.labels(endpoint="/predict").inc()
    PREDICTION_COUNTER.labels(model_version=model_version, prediction_class=prediction).inc()
    CONFIDENCE_HISTOGRAM.observe(confidence)

    # Record latency
    elapsed = time.time() - start_time
    REQUEST_LATENCY_HISTOGRAM.labels(endpoint="/predict").observe(elapsed)

    #Return prediction

    return {
        "result": prediction,
        "confidence": confidence,
        "latency_seconds": elapsed
    }