import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductSearch:

    def __init__(self):

        self.products = pd.read_csv(
            "data/product_metadata.csv"
        )

        self.products["brand"] = (
            self.products["brand"]
            .fillna("")
            .str.lower()
        )

        self.products["product_name"] = (
            self.products["product_name"]
            .fillna("")
            .str.lower()
        )

        self.products["category"] = (
            self.products["category"]
            .fillna("")
            .str.lower()
        )

        self.products["search_text"] = (
            self.products["search_text"]
            .fillna("")
        )

        # Fit TF-IDF vectorizer on search_text for semantic search
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=10000
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.products["search_text"]
        )


    def search_by_id(self, product_id):

        return self.products[
            self.products["product_id"] == product_id
        ]


    def search_by_brand(self, brand):

        brand = brand.lower()

        return self.products[

            self.products["brand"].str.contains(
                brand,
                case=False,
                na=False
            )

        ]


    def search_by_name(self, name):

        name = name.lower()

        return self.products[

            self.products["product_name"].str.contains(
                name,
                case=False,
                na=False
            )

        ]


    def semantic_search(self, query, top_k=10):
        """
        Transform the query with the fitted TF-IDF vectorizer,
        compute cosine similarity against all products, and return
        the top-K results with a similarity_score column.
        Zero-score results are filtered out.
        """

        query_vector = self.vectorizer.transform([query.lower()])

        scores = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        ).flatten()

        # Get top-K indices sorted by descending score
        top_indices = scores.argsort()[::-1][:top_k]

        results = self.products.iloc[top_indices].copy()
        results["similarity_score"] = scores[top_indices]

        # Filter out zero-score results
        results = results[results["similarity_score"] > 0]

        return results.reset_index(drop=True)


    def search_products(self, query, top_k=10):

        query = str(query).strip()

        # Numeric query — try exact ID first, fall through to semantic
        if query.isdigit():

            results = self.search_by_id(int(query))

            if not results.empty:
                return results

        # Free-text — use TF-IDF semantic search
        results = self.semantic_search(query, top_k=top_k)

        return results