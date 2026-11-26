
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Movie Recommendation API")

# Load the trained model and supporting data
with open("recommendation_model.pkl", "rb") as file:
    model = pickle.load(file)

ratings = pd.read_csv("training_ratings.csv")

movies = pd.read_csv(
    r"C:\Users\ASUS\Downloads\archive (6)\movies.csv"
)

@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running"}

@app.get("/recommend/{user_id}")
def recommend(user_id: int, top_n: int = 10):
    if user_id not in ratings["userId"].values:
        raise HTTPException(
            status_code=404,
            detail="User not found in training data"
        )

    watched = set(
        ratings.loc[
            ratings["userId"] == user_id, "movieId"
        ]
    )

    candidates = movies[
        ~movies["movieId"].isin(watched)
    ].copy()

    candidates["predicted_rating"] = candidates[
        "movieId"
    ].apply(
        lambda movie_id: model.predict(
            str(user_id), str(movie_id)
        ).est
    )

    results = candidates.nlargest(
        top_n, "predicted_rating"
    )

    return {
        "user_id": user_id,
        "recommendations": results[
            ["movieId", "title", "predicted_rating"]
        ].to_dict(orient="records")
    }
import time
from monitoring import log_request, write_log

@app.get("/recommend/{user_id}")
def recommend(user_id: int, top_n: int = 10):
    start_time = time.perf_counter()

    try:
        if user_id not in ratings["userId"].values:
            log_request(
                user_id, (time.perf_counter() - start_time) * 1000,
                "error"
            )
            raise HTTPException(
                status_code=404,
                detail="User not found in training data"
            )

        watched = set(
            ratings.loc[
                ratings["userId"] == user_id, "movieId"
            ]
        )

        candidates = movies[
            ~movies["movieId"].isin(watched)
        ].copy()

        candidates["predicted_rating"] = candidates[
            "movieId"
        ].apply(
            lambda movie_id: model.predict(
                str(user_id), str(movie_id)
            ).est
        )

        results = candidates.nlargest(
            top_n, "predicted_rating"
        )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        log_request(
            user_id,
            latency_ms,
            "success",
            len(results)
        )

        return {
            "user_id": user_id,
            "recommendations": results[
                ["movieId", "title", "predicted_rating"]
            ].to_dict(orient="records")
        }

    except HTTPException:
        raise
    except Exception:
        log_request(
            user_id,
            (time.perf_counter() - start_time) * 1000,
            "error"
        )
        raise HTTPException(
            status_code=500,
            detail="Recommendation request failed"
        )

from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import pandas as pd
import joblib
import time
import csv
from datetime import datetime

app = FastAPI(
    title="Movie Recommendation API",
    description="Real-time movie recommendations with API monitoring",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "recommendation_model.pkl"
MOVIES_PATH = Path(r"C:\Users\ASUS\Downloads\archive (6)\movies.csv")
RATINGS_PATH = BASE_DIR / "training_ratings.csv"
LOG_PATH = BASE_DIR / "api_logs.csv"

# Load the trained model
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "Model file not found. Run python train_model.py first."
    )

model = joblib.load(MODEL_PATH)

# Load movie information
if not MOVIES_PATH.exists():
    raise FileNotFoundError(
        f"Movies file not found: {MOVIES_PATH}"
    )

movies = pd.read_csv(MOVIES_PATH)

# Load historical ratings to exclude movies already seen
if RATINGS_PATH.exists():
    ratings = pd.read_csv(RATINGS_PATH)
else:
    ratings = pd.DataFrame(
        columns=["userId", "movieId", "rating"]
    )

# Create the log file if it does not exist
if not LOG_PATH.exists():
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp", "user_id", "latency_ms",
            "status", "recommendations_count"
        ])


def write_log(user_id, latency_ms, status, count):
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            user_id,
            round(latency_ms, 2),
            status,
            count
        ])


@app.get("/")
def home():
    return {
        "message": "Movie Recommendation API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "movies_loaded": len(movies)
    }


@app.get("/recommend/{user_id}")
def recommend(
    user_id: int,
    top_n: int = Query(default=10, ge=1, le=50)
):
    start = time.perf_counter()
    status = 200
    count = 0

    try:
        if user_id <= 0:
            status = 400
            raise HTTPException(
                status_code=400,
                detail="user_id must be a positive integer"
            )

        seen_ids = set()

        if not ratings.empty:
            seen_ids = set(
                ratings.loc[
                    ratings["userId"] == user_id, "movieId"
                ].tolist()
            )

        candidates = movies[
            ~movies["movieId"].isin(seen_ids)
        ]

        if candidates.empty:
            return {
                "user_id": user_id,
                "recommendations": []
            }

        recommendations = []

        for row in candidates.itertuples(index=False):
            prediction = model.predict(
                str(user_id), str(row.movieId)
            )

            recommendations.append({
                "movieId": int(row.movieId),
                "title": row.title,
                "predicted_rating": round(
                    float(prediction.est), 3
                )
            })

        recommendations.sort(
            key=lambda item: item["predicted_rating"],
            reverse=True
        )

        result = recommendations[:top_n]
        count = len(result)

        return {
            "user_id": user_id,
            "recommendations": result
        }

    except HTTPException:
        raise

    except Exception as exc:
        status = 500
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(exc)}"
        )

    finally:
        latency = (
            time.perf_counter() - start
        ) * 1000
        write_log(user_id, latency, status, count)

from datetime import datetime
import csv
import os
from fastapi import Body

CLICK_LOG_PATH = "click_logs.csv"


@app.post("/track-click")
def track_click(payload: dict = Body(...)):
    required = ["user_id", "movie_id", "movie_title"]

    if any(key not in payload for key in required):
        raise HTTPException(
            status_code=400,
            detail="user_id, movie_id, and movie_title are required"
        )

    file_exists = os.path.exists(CLICK_LOG_PATH)

    with open(CLICK_LOG_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "user_id",
                "movie_id",
                "movie_title",
                "event"
            ]
        )

        if not file_exists or os.path.getsize(CLICK_LOG_PATH) == 0:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "user_id": payload["user_id"],
            "movie_id": payload["movie_id"],
            "movie_title": payload["movie_title"],
            "event": "click"
        })

    return {"message": "Click tracked successfully"}
