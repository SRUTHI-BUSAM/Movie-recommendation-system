import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource
def train_model(df):
    tfidf = TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

    vectors = tfidf.fit_transform(df["tags"])

    similarity = cosine_similarity(vectors)

    return similarity


def recommend(movie, df, top_n=4):

    similarity = train_model(df)

    index = df[df["title"] == movie].index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )[1:top_n + 1]

    recommended = []

    for i in scores:
        recommended.append(
            (
                df.iloc[i[0]]["title"],
                round(i[1] * 100, 2)
            )
        )

    return recommended