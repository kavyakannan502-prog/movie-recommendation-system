
import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split

# 1. Load ratings
ratings_path = r"C:\Users\ASUS\Downloads\archive (6)\ratings.csv"
ratings = pd.read_csv(ratings_path)

# 2. Select the required columns
ratings = ratings[["userId", "movieId", "rating"]]

# 3. Define the rating scale
reader = Reader(rating_scale=(0.5, 5.0))

# 4. Convert the data into Surprise format
data = Dataset.load_from_df(ratings, reader)

# 5. Split into training and testing sets
trainset, testset = train_test_split(
    data, test_size=0.2, random_state=42
)

# 6. Train the SVD model
model = SVD(n_factors=50, random_state=42)
model.fit(trainset)

# 7. Evaluate predictions
predictions = model.test(testset)

print("\nMODEL EVALUATION")
accuracy.rmse(predictions)
accuracy.mae(predictions)

print("\nModel training completed successfully!")

# STEP 5: PERSONALIZED MOVIE RECOMMENDATIONS

import pandas as pd

# Load movie information
movies_path = r"C:\Users\ASUS\Downloads\archive (6)\movies.csv"
movies_df = pd.read_csv(movies_path)

# Select a user from the dataset
user_id = ratings["userId"].iloc[0]

# Find movies already rated by this user
rated_movies = set(
    ratings.loc[ratings["userId"] == user_id, "movieId"]
)

# Exclude movies the user has already rated
unrated_movies = movies_df[
    ~movies_df["movieId"].isin(rated_movies)
].copy()

# Predict ratings for unrated movies
unrated_movies["predicted_rating"] = unrated_movies[
    "movieId"
].apply(
    lambda movie_id: model.predict(
        str(user_id), str(movie_id)
    ).est
)

# Select the 10 highest predicted ratings
recommendations = unrated_movies.nlargest(
    10, "predicted_rating"
)

print(f"\nTop 10 recommendations for user {user_id}:")

print(
    recommendations[
        ["title", "predicted_rating"]
    ].to_string(index=False)
)

import pickle

# Save the trained SVD model
with open("recommendation_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save the training ratings for filtering movies already seen
ratings[["userId", "movieId", "rating"]].to_csv(
    "training_ratings.csv", index=False
)

print("\nModel saved as recommendation_model.pkl")
print("Training ratings saved as training_ratings.csv")
