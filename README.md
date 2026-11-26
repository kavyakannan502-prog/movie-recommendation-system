[README.md](https://github.com/user-attachments/files/35450644/README.md)
# movie-recommendation-system
Real-Time Movie Recommendation System using Python, Machine Learning, FastAPI and Streamlit.
# Real-Time Recommendation Service with Monitoring Dashboard

## Project Overview
This project is an end-to-end movie recommendation system that generates personalized movie recommendations using machine learning. It includes a FastAPI service for recommendations, API request logging, and a Streamlit dashboard for monitoring system performance and movie click analytics.

## Features
- Personalized movie recommendations using the SVD collaborative filtering algorithm.
- FastAPI REST API for serving recommendations.
- Exclusion of movies already watched by the user.
- API request logging, including status and response latency.
- Monitoring dashboard with request counts, success rate, latency, and request status.
- Movie click tracking API.
- Click analytics showing total clicks, unique movies clicked, and most-clicked movies.

## Technologies Used
- Python
- Pandas and NumPy
- Scikit-surprise
- FastAPI
- Uvicorn
- Streamlit
- Matplotlib / Plotly (if used in the dashboard)
- MovieLens dataset

## Project Structure
```text
real-time-recommendation-service/
├── app.py
├── dashboard.py
├── train_model.py
├── ratings.csv
├── movies.csv
├── api_logs.csv
├── click_logs.csv
├── requirements.txt
├── README.md
└── .venv/
```

The exact files may vary depending on your setup. The trained model file should also be included in the project structure if your application loads it from disk.

## How to Run

### 1. Activate the virtual environment
Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

### 3. Start the recommendation API
```powershell
uvicorn app:app --reload
```

Open the API documentation:
http://127.0.0.1:8000/docs

### 4. Start the monitoring dashboard
Open a second terminal in the project folder, activate the virtual environment, and run:
```powershell
python -m streamlit run dashboard.py
```

Open the dashboard at:
http://localhost:8501

## API Endpoints
- `GET /recommend/{user_id}` — retrieves movie recommendations for a user.
- `POST /track-click` — records a movie click for analytics.

Use the interactive API documentation at `/docs` to test the endpoints.

## Model Evaluation
The trained SVD model previously achieved:
- RMSE: approximately 0.8661
- MAE: approximately 0.6708

These are the recorded evaluation results from the current project; verify them against your latest model run before presenting them.

## Future Improvements
- Add recommendation quality and user engagement metrics.
- Implement data and model drift monitoring.
- Add automated alerts for API failures.
- Deploy the service to a cloud platform.

## Author
Kavya Kannan
