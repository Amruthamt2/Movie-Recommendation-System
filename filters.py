def apply_age_filter(recommendations, age_group):
    """
    Filters recommendations based on age group.
    Below 18 users should not receive Horror, Crime or Thriller movies.
    """

    if age_group == "18 and Above":
        return recommendations

    blocked_genres = ["Horror", "Crime", "Thriller"]

    filtered = []

    for movie in recommendations:

        blocked = False

        for genre in blocked_genres:

            if genre.lower() in movie["genres"].lower():
                blocked = True
                break

        if not blocked:
            filtered.append(movie)

    return filtered


def apply_genre_filter(recommendations, selected_genre):
    """
    Filters recommendations by the selected genre.
    """

    if selected_genre == "All":
        return recommendations

    filtered = []

    for movie in recommendations:

        if selected_genre.lower() in movie["genres"].lower():
            filtered.append(movie)

    # If no matching movies exist, return the original list
    if len(filtered) == 0:
        return recommendations

    return filtered