
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Recommendation Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation Dashboard")
st.write("Real-Time Recommendation Service")

user_id = st.number_input(
    "Enter User ID",
    min_value=1,
    value=1,
    step=1
)

top_n = st.slider(
    "Number of recommendations",
    min_value=5,
    max_value=20,
    value=10
)

if st.button("Get Recommendations"):
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/recommend/{user_id}",
            params={"top_n": top_n},
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        recommendations = data.get("recommendations", [])

        if recommendations:
            df = pd.DataFrame(recommendations)

            st.success("Recommendations loaded successfully!")
            st.metric("Movies Recommended", len(df))
            st.dataframe(df, use_container_width=True)

            if "predicted_rating" in df.columns:
                st.bar_chart(
                    df.set_index("title")["predicted_rating"]
                )
        else:
            st.warning("No recommendations returned.")

    except requests.RequestException as error:
        st.error(f"Could not connect to the API: {error}")
    except (ValueError, KeyError) as error:
        st.error(f"Unexpected API response: {error}")

# ---------------- API MONITORING DASHBOARD ----------------

from pathlib import Path
import pandas as pd

st.divider()
st.header("API Monitoring & Performance")

LOG_FILE = Path(__file__).with_name("api_logs.csv")

if LOG_FILE.exists():
    logs = pd.read_csv(LOG_FILE)

    if not logs.empty:
        # Convert metric columns to numeric values
        logs["latency_ms"] = pd.to_numeric(
            logs["latency_ms"], errors="coerce"
        )
        logs["status"] = pd.to_numeric(
            logs["status"], errors="coerce"
        )
        logs["recommendations_count"] = pd.to_numeric(
            logs["recommendations_count"], errors="coerce"
        )

        total_requests = len(logs)
        avg_latency = logs["latency_ms"].mean()
        successful_requests = (logs["status"] == 200).sum()
        failed_requests = (logs["status"] != 200).sum()
        success_rate = successful_requests / total_requests * 100
        total_recommendations = logs[
            "recommendations_count"
        ].fillna(0).sum()

                # Display key metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total API Requests", total_requests)
        col2.metric(
            "Average Latency",
            f"{avg_latency:.2f} ms"
        )
        col3.metric("Success Rate", f"{success_rate:.1f}%")
        col4.metric(
            "Recommendations Served",
            int(total_recommendations)
        )
        col5.metric("Failed Requests", int(failed_requests))

        # Prepare timestamp for charts
        if "timestamp" in logs.columns:
            logs["timestamp"] = pd.to_datetime(
                logs["timestamp"], errors="coerce"
            )

            chart_data = logs.dropna(
                subset=["timestamp", "latency_ms"]
            ).sort_values("timestamp")

            if not chart_data.empty:
                st.subheader("API Latency Over Time")
                st.line_chart(
                    chart_data.set_index("timestamp")["latency_ms"]
                )

        st.subheader("Recent API Requests")
        st.dataframe(logs.tail(20), use_container_width=True)

        # Allow manual refresh
        if st.button("Refresh Monitoring Metrics"):
            st.rerun()

        
        
else:
    st.warning("api_logs.csv was not found in the project folder.")

# API Request Status Distribution
st.subheader("API Request Status Distribution")

if not logs.empty:
    status_counts = (
        logs["status"]
        .astype(str)
        .value_counts()
        .sort_index()
    )

    st.bar_chart(status_counts)
else:
    st.info("No API requests logged yet.")


    
# Movie Click Analytics
st.divider()
st.header("Movie Click Analytics")

from pathlib import Path

click_file = Path(__file__).parent / "click_logs.csv"

if click_file.exists():
    try:
        clicks = pd.read_csv(click_file)

        if not clicks.empty and "movie_title" in clicks.columns:
            total_clicks = len(clicks)
            unique_movies = clicks["movie_id"].nunique() if "movie_id" in clicks.columns else clicks["movie_title"].nunique()

            most_clicked = (
                clicks["movie_title"].value_counts().idxmax()
                if total_clicks > 0 else "N/A"
            )

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Movie Clicks", total_clicks)
            col2.metric("Unique Movies Clicked", unique_movies)
            col3.metric("Most-Clicked Movie", most_clicked)

            st.subheader("Most-Clicked Movies")
            st.bar_chart(clicks["movie_title"].value_counts().head(10))
        else:
            st.info("No movie click records available yet.")
    except Exception as e:
        st.error(f"Could not read click_logs.csv: {e}")
else:
    st.info("click_logs.csv was not found.")

