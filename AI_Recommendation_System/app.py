import json
import streamlit as st

from recommendation.engine import get_recommendations


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Recommendation System",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

def load_items():
    with open("data/items.json", "r", encoding="utf-8") as file:
        return json.load(file)


items = load_items()


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("🤖 AI Recommendation System")

st.write(
    "A personalized recommendation system based on "
    "user preferences and similarity matching."
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("🎯 Your Preferences")

st.sidebar.write(
    "Select the topics you are interested in."
)


# Get all unique tags

all_interests = sorted(
    {
        tag
        for item in items
        for tag in item["tags"]
    }
)


selected_interests = st.sidebar.multiselect(
    "Choose your interests:",
    all_interests
)


# --------------------------------------------------
# Recommendation Button
# --------------------------------------------------

if st.sidebar.button("🔍 Get Recommendations"):

    if not selected_interests:

        st.warning(
            "Please select at least one interest."
        )

    else:

        recommendations = get_recommendations(
            selected_interests,
            items
        )

        st.subheader("🎯 Recommended For You")

        # Show only recommendations with a score

        useful_recommendations = [
            recommendation
            for recommendation in recommendations
            if recommendation["score"] > 0
        ]

        if not useful_recommendations:

            st.info(
                "No matching recommendations were found."
            )

        else:

            for recommendation in useful_recommendations:

                item = recommendation["item"]

                score = recommendation["score"]

                matched_tags = recommendation["matched_tags"]


                # Recommendation card

                with st.container():

                    st.markdown(
                        f"### 📚 {item['name']}"
                    )

                    st.write(
                        f"**Category:** {item['category']}"
                    )

                    st.write(
                        item["description"]
                    )

                    st.progress(
                        min(int(score), 100)
                    )

                    st.write(
                        f"**Similarity Score:** {score}%"
                    )

                    if matched_tags:

                        st.write(
                            "**Matched Interests:** "
                            + ", ".join(matched_tags)
                        )

                    st.divider()


# --------------------------------------------------
# Information Section
# --------------------------------------------------

st.subheader("ℹ️ How It Works")

st.write(
    """
    The recommendation engine compares your selected
    interests with the tags associated with each item.

    A similarity score is calculated based on the number
    of matching interests.

    Items with higher similarity scores are displayed
    first.
    """
)