import pandas as pd

catalog = pd.read_csv(
    "data/product_catalog.csv"
)

metadata = pd.read_csv(
    "data/product_metadata.csv"
)


def get_product_details(product_id):

    product = catalog[
        catalog["product_id"] == product_id
    ]

    if product.empty:
        return None

    row = product.iloc[0]

    # Fetch product_name from metadata if available
    meta_row = metadata[
        metadata["product_id"] == product_id
    ]

    product_name = (
        meta_row.iloc[0]["product_name"]
        if not meta_row.empty
        else f"Product {product_id}"
    )

    price_bucket = (
        meta_row.iloc[0]["price_bucket"]
        if not meta_row.empty and "price_bucket" in meta_row.columns
        else "Unknown"
    )

    return {
        "product_id": int(row["product_id"]),
        "product_name": str(product_name),
        "brand": str(row["brand"]),
        "category": str(row["category_code"]),
        "price": float(row["price"]),
        "price_bucket": str(price_bucket),
    }


def generate_explanation(
    product_id,
    content_score,
    collab_score,
    popularity_score,
    hybrid_score
):
    """
    Returns a detailed explanation dict for a recommended product,
    including individual model contribution scores and a primary reason.

    Args:
        product_id: The recommended product's ID.
        content_score: Normalized content-based similarity score (0–1).
        collab_score: Normalized collaborative filtering score (0–1).
        popularity_score: Normalized popularity score (0–1).
        hybrid_score: Final weighted hybrid score (0–1).

    Returns:
        dict with keys: content_score, collaborative_score,
        popularity_score, hybrid_score, reason, reasons (list)
    """

    reasons = []

    if collab_score > 0:
        reasons.append("Frequently Purchased Together")

    if content_score > 0:
        reasons.append("Similar Brand & Category")

    if popularity_score > 0:
        reasons.append("Popular Product")

    if not reasons:
        reasons.append("Trending Product")

    # Primary reason (highest priority)
    reason = reasons[0]

    return {
        "content_score": round(content_score, 4),
        "collaborative_score": round(collab_score, 4),
        "popularity_score": round(popularity_score, 4),
        "hybrid_score": round(hybrid_score, 4),
        "reason": reason,
        "reasons": reasons,
    }


# Legacy wrapper — kept for backwards compatibility
def generate_reason(
    product_id,
    content_scores,
    collab_scores,
    popular_scores
):

    reasons = []

    if product_id in collab_scores:
        reasons.append("Frequently Purchased Together")

    if product_id in content_scores:
        reasons.append("Similar Brand & Category")

    if product_id in popular_scores:
        reasons.append("Popular Product")

    return reasons