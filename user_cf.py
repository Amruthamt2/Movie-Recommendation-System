import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load Data
ratings = pd.read_csv("data/ratings.csv")
movies = pd.read_csv("data/movies.csv")

# User-Movie Matrix
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)

# User Similarity Matrix
user_similarity = cosine_similarity(user_movie_matrix)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)


def get_user_recommendations(user_id, top_n=10):
    """
    User-Based Collaborative Filtering
    """

    # Similar users
    similar_users = user_similarity_df[user_id].sort_values(
        ascending=False
    )[1:6]

    # Movies already watched
    watched_movies = set(
        ratings[ratings["userId"] == user_id]["movieId"]
    )

    movie_scores = {}

    # Collect recommendations
    for sim_user in similar_users.index:

        sim_ratings = ratings[
            ratings["userId"] == sim_user
        ]

        for _, row in sim_ratings.iterrows():

            movie_id = row["movieId"]

            if movie_id not in watched_movies:

                movie_scores[movie_id] = movie_scores.get(
                    movie_id,
                    0
                ) + row["rating"]

    # Sort by score
    ranked_movies = sorted(
        movie_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for movie_id, score in ranked_movies[:top_n]:

        movie = movies[movies["movieId"] == movie_id]

        if not movie.empty:

            recommendations.append({
                "movieId": int(movie_id),
                "title": movie.iloc[0]["title"],
                "genres": movie.iloc[0]["genres"],
                "score": round(score, 2)
            })

    return recommendations


# Test
if __name__ == "__main__":

    recs = get_user_recommendations(1)

    print("\nTop Recommendations\n")

    for movie in recs:
        print(movie)