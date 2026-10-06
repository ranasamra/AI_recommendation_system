def calculate_similarity(user_interests, item_tags):
    """
    Calculate similarity between user interests and item tags.

    Similarity Score =
    Number of matching interests / Number of item tags × 100
    """

    user_interests = {
        interest.strip().lower()
        for interest in user_interests
    }

    item_tags_normalized = {
        tag.strip().lower()
        for tag in item_tags
    }

    matching_tags = user_interests.intersection(item_tags_normalized)

    if not item_tags_normalized:
        return 0, []

    score = (len(matching_tags) / len(item_tags_normalized)) * 100

    return round(score, 2), list(matching_tags)


def get_recommendations(user_interests, items):
    """
    Generate recommendations based on similarity scores.
    """

    recommendations = []

    for item in items:
        score, matched_tags = calculate_similarity(
            user_interests,
            item["tags"]
        )

        recommendations.append({
            "item": item,
            "score": score,
            "matched_tags": matched_tags
        })

    recommendations.sort(
        key=lambda recommendation: recommendation["score"],
        reverse=True
    )

    return recommendations