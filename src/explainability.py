import pandas as pd

catalog = pd.read_csv(
    "data/product_catalog.csv"
)

def get_product_details(product_id):

    product = catalog[
        catalog["product_id"] == product_id
    ]

    if product.empty:
        return None

    row = product.iloc[0]

    return {
        "product_id": int(row["product_id"]),
        "brand": str(row["brand"]),
        "category": str(row["category_code"]),
        "price": float(row["price"])
    }


def generate_reason(
    product_id,
    content_scores,
    collab_scores,
    popular_scores
):

    reasons = []

    if product_id in collab_scores:
        reasons.append(
            "Collaborative Recommendation"
        )

    if product_id in content_scores:
        reasons.append(
            "Similar Product Recommendation"
        )

    if product_id in popular_scores:
        reasons.append(
            "Popular Product"
        )

    return reasons