import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load catalog once
catalog = pd.read_csv("data/product_catalog.csv")

catalog["brand"] = catalog["brand"].fillna("Unknown_Brand")
catalog["category_code"] = catalog["category_code"].fillna("Unknown_Category")

catalog["features"] = (
    catalog["brand"] + " " +
    catalog["category_code"]
)

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(
    catalog["features"]
)


def get_content_recommendations(product_id, top_n=5):

    if product_id not in catalog["product_id"].values:
        return {}

    idx = catalog[
        catalog["product_id"] == product_id
    ].index[0]

    product_vector = tfidf_matrix[idx]

    similarities = cosine_similarity(
        product_vector,
        tfidf_matrix
    ).flatten()

    top_indices = similarities.argsort()[::-1][1:top_n+1]

    recommendations = {}

    for i in top_indices:

        row = catalog.iloc[i]

        recommendations[
            int(row["product_id"])
        ] = float(similarities[i])

    return recommendations


# Testing
if __name__ == "__main__":

    recs = get_content_recommendations(
        1004237
    )

    print("\nContent Recommendations:\n")

    for product, score in recs.items():

        print(
            f"Product: {product} | Similarity: {score:.4f}"
        )