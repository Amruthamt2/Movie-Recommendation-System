import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load Data
ratings = pd.read_csv("data/ratings.csv")
movies = pd.read_csv("data/movies.csv")

# Create Movie-User Matrix
movie_user_matrix = ratings.pivot_table(
    index="movieId",
    columns="userId",
    values="rating"
).fillna(0)

# Calculate Movie Similarity
movie_similarity = cosine_similarity(movie_user_matrix)

movie_similarity_df = pd.DataFrame(
    movie_similarity,
    index=movie_user_matrix.index,
    columns=movie_user_matrix.index
)


def get_item_recommendations(user_id, top_n=10):
    """
    Item-Based Collaborative Filtering
    """

    # Movies watched by the user
    watched_movies = ratings[
        ratings["userId"] == user_id
    ]["movieId"].tolist()

    movie_scores = {}

    # Find similar movies
    for movie in watched_movies:

        if movie not in movie_similarity_df.index:
            continue

        similar_movies = movie_similarity_df[movie].sort_values(
            ascending=False
        )[1:11]

        for sim_movie, similarity in similar_movies.items():

            if sim_movie not in watched_movies:

                movie_scores[sim_movie] = movie_scores.get(
                    sim_movie,
                    0
                ) + similarity

    # Sort by similarity score
    ranked_movies = sorted(
        movie_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for movie_id, score in ranked_movies[:top_n]:

        movie = movies[
            movies["movieId"] == movie_id
        ]

        if not movie.empty:

            recommendations.append({
                "movieId": int(movie_id),
                "title": movie.iloc[0]["title"],
                "genres": movie.iloc[0]["genres"],
                "score": round(float(score), 3)
            })

    return recommendations


# Test
if __name__ == "__main__":

    recs = get_item_recommendations(1)

    print("\nTop Item-Based Recommendations\n")

    for movie in recs:
        print(movie)