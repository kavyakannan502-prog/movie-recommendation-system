
import pandas as pd

# File paths
ratings_path = r"C:\Users\ASUS\Downloads\archive (6)\ratings.csv"
movies_path = r"C:\Users\ASUS\Downloads\archive (6)\movies.csv"

# Load the datasets
ratings = pd.read_csv(ratings_path)
movies = pd.read_csv(movies_path)

# Display basic information
print("Ratings dataset shape:", ratings.shape)
print("Movies dataset shape:", movies.shape)

print("\nRatings columns:")
print(ratings.columns.tolist())

print("\nMovies columns:")
print(movies.columns.tolist())

print("\nFirst five ratings:")
print(ratings.head())

print("\nFirst five movies:")
print(movies.head())

# STEP 2: Exploratory Data Analysis (EDA)

print("\n========== DATASET INFORMATION ==========")

print("\nRatings dataset information:")
print(ratings.info())

print("\nMovies dataset information:")
print(movies.info())

print("\nMissing values in ratings:")
print(ratings.isnull().sum())

print("\nMissing values in movies:")
print(movies.isnull().sum())

print("\nDuplicate rows in ratings:", ratings.duplicated().sum())
print("Duplicate rows in movies:", movies.duplicated().sum())

print("\nRating statistics:")
print(ratings["rating"].describe())

# Count how many ratings each movie received
movie_counts = ratings["movieId"].value_counts()

# Get the 10 most frequently rated movies
top_movie_ids = movie_counts.head(10).index

# Match movie IDs with movie titles
top_movies = movies[
    movies["movieId"].isin(top_movie_ids)
].copy()

top_movies["number_of_ratings"] = top_movies["movieId"].map(
    movie_counts
)

top_movies = top_movies.sort_values(
    "number_of_ratings", ascending=False
)

print("\n========== TOP 10 POPULAR MOVIES ==========")
print(top_movies[["title", "number_of_ratings"]].to_string(index=False))

# Count ratings received by each movie
movie_counts = ratings.groupby("movieId").size()

# Get the 10 most frequently rated movies
top_movie_ids = movie_counts.nlargest(10).index

# Match movie IDs to their titles
top_movies = movies[
    movies["movieId"].isin(top_movie_ids)
].copy()

top_movies["number_of_ratings"] = (
    top_movies["movieId"].map(movie_counts)
)

top_movies = top_movies.sort_values(
    "number_of_ratings", ascending=False
)

print("\nTOP 10 MOST POPULAR MOVIES")
print(
    top_movies[["title", "number_of_ratings"]]
    .to_string(index=False)
)


import matplotlib.pyplot as plt

rating_counts = ratings["rating"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
plt.bar(rating_counts.index.astype(str), rating_counts.values)

plt.title("Distribution of Movie Ratings")
plt.xlabel("Rating")
plt.ylabel("Number of Ratings")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

print("\nRatings columns:")
print(ratings.columns.tolist())

print("\nMovies columns:")
print(movies.columns.tolist())

print("\nRatings columns:", ratings.columns.tolist())
print("Movies columns:", movies.columns.tolist())

print("\nTotal ratings:", len(ratings))
print("Unique users:", ratings.iloc[:, 0].nunique())
print("Unique movies:", ratings.iloc[:, 1].nunique())

