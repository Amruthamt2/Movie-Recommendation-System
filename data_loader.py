import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
ratings = pd.read_csv("data/ratings.csv")
movies = pd.read_csv("data/movies.csv")

# Create User-Movie Matrix
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)

# Create Movie-User Matrix
movie_user_matrix = ratings.pivot_table(
    index="movieId",
    columns="userId",
    values="rating"
).fillna(0)

# User Similarity Matrix
user_similarity = cosine_similarity(user_movie_matrix)

# Movie Similarity Matrix
movie_similarity = cosine_similarity(movie_user_matrix)

# Dataset Statistics
TOTAL_USERS = ratings["userId"].nunique()
TOTAL_MOVIES = movies["movieId"].nunique()
TOTAL_RATINGS = len(ratings)


def load_data():
    return (
        ratings,
        movies,
        user_movie_matrix,
        movie_user_matrix,
        user_similarity,
        movie_similarity,
    )


# Test
if __name__ == "__main__":
    print("Dataset Loaded Successfully")
    print(f"Users   : {TOTAL_USERS}")
    print(f"Movies  : {TOTAL_MOVIES}")
    print(f"Ratings : {TOTAL_RATINGS}")