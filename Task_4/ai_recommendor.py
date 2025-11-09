import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


movies = pd.DataFrame({
    'movie_id': [1, 2, 3, 4, 5],
    'title': ['The Matrix', 'Inception', 'Gladiator', 'Frozen', 'La La Land'],
    'genres': ['Sci-Fi Action', 'Sci-Fi Thriller', 'Historical Drama', 'Animation Fantasy', 'Romantic Musical']
})

ratings = pd.DataFrame({
    'user_id': [1, 1, 1, 2, 2, 3, 3, 3],
    'movie_id': [1, 2, 3, 2, 4, 1, 4, 5],
    'rating': [5, 4, 5, 3, 4, 4, 5, 3]
})


vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(movies['genres'])
cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_content_recommendations(movie_title, top_n=3):
    if movie_title not in movies['title'].values:
        return ["That movie isn't in our database."]
    idx = movies[movies['title'] == movie_title].index[0]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:top_n+1]]
    return movies.iloc[top_indices]['title'].tolist()


ratings_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating')
similarity_scores = cosine_similarity(ratings_matrix.fillna(0))
similarity_df = pd.DataFrame(similarity_scores, index=ratings_matrix.index, columns=ratings_matrix.index)

def get_collaborative_recommendations(user_id, top_n=3):
    if user_id not in ratings_matrix.index:
        return ["Invalid user ID. Try 1, 2, or 3."]
    similar_users = similarity_df[user_id].sort_values(ascending=False).index[1:]
    target_ratings = ratings_matrix.loc[user_id]
    recs = pd.Series(dtype=float)

    for other_user in similar_users:
        weight = similarity_df[user_id][other_user]
        other_ratings = ratings_matrix.loc[other_user]
        weighted = other_ratings * weight
        recs = recs.add(weighted, fill_value=0)

    recs = recs.drop(target_ratings[target_ratings.notna()].index, errors='ignore')
    top_movies = recs.sort_values(ascending=False).head(top_n).index
    return movies[movies['movie_id'].isin(top_movies)]['title'].tolist()


def hybrid_recommender(user_id, liked_movie):
    content_recs = get_content_recommendations(liked_movie, top_n=3)
    collab_recs = get_collaborative_recommendations(user_id, top_n=3)
    combined = content_recs + collab_recs
    final = pd.Series(combined).value_counts().index.tolist()
    return final[:3]


if __name__ == "__main__":
    print("🎞️ Welcome to CineMatch 2.0 — Smart Movie Suggestions!")
    print("Movies available:", ', '.join(movies['title'].values))
    print("Registered users: 1, 2, 3")
    print("=" * 60)

    while True:
        user_input = input("Enter User ID (1-3) or 'q' to quit: ").strip()
        if user_input.lower() == 'q':
            print("👋 Thanks for using CineMatch 2.0! See you next time.")
            break

        if not user_input.isdigit():
            print("⚠️ Please enter a numeric user ID (1-3).")
            continue

        user_id = int(user_input)
        liked_movie = input("Enter a movie you liked: ").strip()

        print("\n🎯 Recommended Movies for You:")
        suggestions = hybrid_recommender(user_id, liked_movie)
        for i, movie in enumerate(suggestions, 1):
            print(f"{i}. {movie}")
        print("=" * 60)
