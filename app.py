import streamlit as st
import pandas as pd

from data_loader import (
    TOTAL_USERS,
    TOTAL_MOVIES,
    TOTAL_RATINGS
)

from user_cf import get_user_recommendations
from item_cf import get_item_recommendations

from filters import (
    apply_age_filter,
    apply_genre_filter
)

from evaluation import (
    calculate_metrics,
    comparison_table
)

# ------------------------------------
# PAGE CONFIG
# ------------------------------------

st.set_page_config(
    page_title="Hybrid Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ------------------------------------
# SIDEBAR
# ------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Evaluation"
    ]
)

# ====================================
# DASHBOARD
# ====================================

if page == "Dashboard":

    st.title("🎬 Hybrid Movie Recommendation System")

    st.write(
        "Movie recommendation using User-Based and Item-Based Collaborative Filtering."
    )

    st.markdown("---")

    # Statistics

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "👥 Users",
        TOTAL_USERS
    )

    c2.metric(
        "🎬 Movies",
        TOTAL_MOVIES
    )

    c3.metric(
        "⭐ Ratings",
        TOTAL_RATINGS
    )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        age_group = st.selectbox(

            "Age Group",

            [
                "Below 18",
                "18 and Above"
            ]

        )

        gender = st.selectbox(

            "Gender",

            [
                "Male",
                "Female",
                "Other"
            ]

        )

        user_id = st.selectbox(

            "User ID",

            list(range(1,611))

        )

    with right:

        genre = st.selectbox(

            "Favorite Genre",

            [
                "All",
                "Action",
                "Adventure",
                "Animation",
                "Comedy",
                "Crime",
                "Drama",
                "Fantasy",
                "Horror",
                "Romance",
                "Sci-Fi",
                "Thriller"
            ]

        )

        algorithm = st.selectbox(

            "Recommendation Algorithm",

            [
                "User-Based CF",
                "Item-Based CF"
            ]

        )

    st.markdown("---")
    if st.button("🎯 Get Recommendations"):

        # Choose Algorithm

        if algorithm == "User-Based CF":

            recommendations = get_user_recommendations(user_id)

        else:

            recommendations = get_item_recommendations(user_id)

        # Apply Filters

        recommendations = apply_age_filter(
            recommendations,
            age_group
        )

        recommendations = apply_genre_filter(
            recommendations,
            genre
        )

        st.success("Recommendations Generated Successfully")

        st.markdown("---")

        st.subheader("👤 User Profile")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**User ID:** {user_id}")
            st.write(f"**Age Group:** {age_group}")
            st.write(f"**Gender:** {gender}")

        with col2:
            st.write(f"**Favorite Genre:** {genre}")
            st.write(f"**Algorithm:** {algorithm}")

        st.markdown("---")

        st.subheader("🎬 Top Recommended Movies")

        if len(recommendations) == 0:

            st.warning("No recommendations found.")

        else:

            for i, movie in enumerate(recommendations, start=1):

                with st.container():

                    st.markdown(f"### {i}. 🎬 {movie['title']}")

                    st.write(f"**Genres:** {movie['genres']}")

                    st.write(f"**Recommendation Score:** {movie['score']}")

                    st.markdown("---")
                    # ====================================
# EVALUATION PAGE
# ====================================

elif page == "Evaluation":

    st.title("📊 Evaluation Dashboard")

    metrics = calculate_metrics()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Precision",
        metrics["Precision"]
    )

    c2.metric(
        "Recall",
        metrics["Recall"]
    )

    c3.metric(
        "F1 Score",
        metrics["F1 Score"]
    )

    st.markdown("---")

    st.subheader("📈 Algorithm Comparison")

    comparison = comparison_table()

    st.dataframe(
        comparison,
        use_container_width=True
    )

    st.bar_chart(
        comparison.set_index("Algorithm")
    )

    st.markdown("---")

    st.subheader("📌 Project Summary")

    st.success(
        """
        ✔ User-Based Collaborative Filtering

        ✔ Item-Based Collaborative Filtering

        ✔ Age-Based Filtering

        ✔ Genre-Based Filtering

        ✔ Evaluation using Precision, Recall and F1 Score
        """
    )

    st.markdown("---")

    st.info(
        """
        **Hybrid Movie Recommendation System**

        This project recommends movies using Collaborative
        Filtering techniques.

        • User-Based Collaborative Filtering

        • Item-Based Collaborative Filtering

        • Age Group Filter

        • Favorite Genre Filter

        • Streamlit Dashboard

        • Evaluation Metrics
        """
    )