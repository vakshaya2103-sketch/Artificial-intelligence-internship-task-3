"""
Project 3: AI Recommendation Logic
====================================

Goal:
    Create a simple recommendation system based on user preferences.

Key Requirements covered:
    1. Take user input (choices or interests)
    2. Match preferences using logic or similarity
    3. Display recommended items

Key Skills demonstrated:
    Logic building, pattern matching, recommendation concepts.

Approach:
    This is a "content-based" recommender — the simplest, most
    explainable type of recommendation system. Each item (a movie, in
    this example) is tagged with genres/attributes. The user picks the
    genres they like, and we score every item by how much it overlaps
    with the user's interests using Jaccard similarity (a standard
    set-overlap measure used in real recommender systems).

    No machine learning model is required for this — it's pure logic
    and math, which is exactly what "pattern matching using logic or
    similarity" means at this level.

Author: (Your Name Here)
"""


# ---------------------------------------------------------------------------
# 1. THE ITEM CATALOG (small dataset of items + their attributes/tags)
# ---------------------------------------------------------------------------
# In a real system this would come from a database or CSV. Here it's a
# small in-memory dataset so the project runs instantly with no setup.

MOVIES = [
    {"title": "Galactic Frontier",      "genres": {"sci-fi", "action", "adventure"}},
    {"title": "The Last Algorithm",     "genres": {"sci-fi", "thriller", "drama"}},
    {"title": "Laugh Track",            "genres": {"comedy", "romance"}},
    {"title": "Midnight Heist",         "genres": {"action", "thriller", "crime"}},
    {"title": "Whispering Woods",       "genres": {"horror", "thriller"}},
    {"title": "Two Hearts, One Coffee", "genres": {"romance", "comedy", "drama"}},
    {"title": "Code Red Protocol",      "genres": {"action", "sci-fi", "thriller"}},
    {"title": "The Quiet Garden",       "genres": {"drama", "family"}},
    {"title": "Starlight Odyssey",      "genres": {"sci-fi", "adventure", "family"}},
    {"title": "Haunted Hollow",         "genres": {"horror", "mystery"}},
    {"title": "Boardroom Wars",         "genres": {"drama", "thriller"}},
    {"title": "Sunday Funday",          "genres": {"comedy", "family"}},
]

ALL_GENRES = sorted({genre for movie in MOVIES for genre in movie["genres"]})


# ---------------------------------------------------------------------------
# 2. TAKE USER INPUT (choices / interests)
# ---------------------------------------------------------------------------
def get_user_preferences() -> set:
    """
    Asks the user to pick their favorite genres from the available list.
    Returns a set of chosen genres (e.g. {"sci-fi", "action"}).

    Input validation is included: invalid genres are ignored with a
    warning instead of crashing the program.
    """
    print("Available genres:")
    print(", ".join(ALL_GENRES))
    print()

    raw_input_text = input(
        "Enter your favorite genres, separated by commas (e.g. sci-fi, comedy): "
    )

    chosen = {g.strip().lower() for g in raw_input_text.split(",") if g.strip()}
    valid_choices = chosen & set(ALL_GENRES)
    invalid_choices = chosen - set(ALL_GENRES)

    if invalid_choices:
        print(f"\n(Note: ignoring unrecognized genres: {', '.join(invalid_choices)})")

    if not valid_choices:
        print("No valid genres entered — defaulting to a popular pick: 'drama'.")
        valid_choices = {"drama"}

    print(f"\nYour selected interests: {', '.join(sorted(valid_choices))}\n")
    return valid_choices


# ---------------------------------------------------------------------------
# 3. MATCH PREFERENCES USING LOGIC / SIMILARITY
# ---------------------------------------------------------------------------
def jaccard_similarity(set_a: set, set_b: set) -> float:
    """
    Computes Jaccard similarity between two sets:

        similarity = |intersection| / |union|

    This is a simple, well-known similarity measure: it returns 1.0 for
    identical sets, 0.0 for completely unrelated sets, and a value in
    between based on how much overlap there is. It's a standard building
    block in real-world recommendation systems.
    """
    if not set_a or not set_b:
        return 0.0

    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def recommend_movies(user_genres: set, catalog: list, top_n: int = 5) -> list:
    """
    Scores every movie in the catalog against the user's chosen genres
    using Jaccard similarity, then returns the top_n highest-scoring
    movies (ties broken by catalog order).

    Movies with zero overlap (score = 0) are excluded entirely — there's
    no point recommending something with nothing in common.
    """
    scored_movies = []

    for movie in catalog:
        score = jaccard_similarity(user_genres, movie["genres"])
        if score > 0:
            scored_movies.append((movie["title"], movie["genres"], score))

    # Sort by similarity score, descending (highest match first)
    scored_movies.sort(key=lambda item: item[2], reverse=True)

    return scored_movies[:top_n]


# ---------------------------------------------------------------------------
# 4. DISPLAY RECOMMENDED ITEMS
# ---------------------------------------------------------------------------
def display_recommendations(recommendations: list) -> None:
    """
    Nicely prints the final list of recommended movies, including their
    genres and how strong the match was (as a percentage).
    """
    print("=" * 60)
    print(" YOUR RECOMMENDATIONS")
    print("=" * 60)

    if not recommendations:
        print("No matching movies found for your interests. Try different genres!")
        return

    for rank, (title, genres, score) in enumerate(recommendations, start=1):
        match_pct = score * 100
        genre_text = ", ".join(sorted(genres))
        print(f"{rank}. {title}")
        print(f"   Genres: {genre_text}")
        print(f"   Match strength: {match_pct:.0f}%\n")


# ---------------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print(" AI MOVIE RECOMMENDATION SYSTEM")
    print("=" * 60)
    print("Tell us what you like, and we'll recommend movies for you!\n")

    user_genres = get_user_preferences()
    recommendations = recommend_movies(user_genres, MOVIES, top_n=5)
    display_recommendations(recommendations)

    print("Thanks for using the recommender! Run again anytime for new picks.")


if __name__ == "__main__":
    main()
