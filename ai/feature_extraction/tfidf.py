from sklearn.feature_extraction.text import TfidfVectorizer


def build_tfidf_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)

