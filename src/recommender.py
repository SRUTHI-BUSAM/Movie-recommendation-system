from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_model(df):
    tfidf = TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

    vectors = tfidf.fit_transform(df["tags"])

    return tfidf, vectors


def recommend(movie, df, tfidf, vectors, top_n=4):

    index = df[df["title"] == movie].index[0]

    movie_vector = vectors[index]

    scores = cosine_similarity(
        movie_vector,
        vectors
    ).flatten()

    top_indices = scores.argsort()[::-1][1:top_n + 1]

    recommended = []

    for i in top_indices:
        recommended.append(
            (
                df.iloc[i]["title"],
                round(scores[i] * 100, 2)
            )
        )

    return recommended