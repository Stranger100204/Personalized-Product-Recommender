from src.content_based import get_content_recommendations
from src.item_collaborative import get_collaborative_recommendations
from src.popularity import get_popular_products
from src.explainability import (
    get_product_details,
    generate_reason
)

def get_hybrid_recommendations(product_id, top_n=10):

    # Get recommendation scores
    content_scores = get_content_recommendations(
        product_id,
        top_n=5
    )

    collab_scores = get_collaborative_recommendations(
        product_id,
        top_n=5
    )

    popular_scores = get_popular_products(
        top_n=10
    )

    if not isinstance(content_scores, dict):
        content_scores = {}

    if not isinstance(collab_scores, dict):
        collab_scores = {}

    if not isinstance(popular_scores, dict):
        popular_scores = {}

    # Normalize content scores
    if content_scores:

        max_content = max(
            content_scores.values()
        )

        content_scores = {
            product: score / max_content
            for product, score in content_scores.items()
        }

    # Normalize collaborative scores
    if collab_scores:

        max_collab = max(
            collab_scores.values()
        )

        collab_scores = {
            product: score / max_collab
            for product, score in collab_scores.items()
        }

    # Normalize popularity scores
    if popular_scores:

        max_popular = max(
            popular_scores.values()
        )

        popular_scores = {
            product: score / max_popular
            for product, score in popular_scores.items()
        }

    # Combine products
    all_products = (
        set(content_scores.keys())
        |
        set(collab_scores.keys())
        |
        set(popular_scores.keys())
    )

    hybrid_scores = {}

    for product in all_products:

        content = content_scores.get(
            product,
            0
        )

        collab = collab_scores.get(
            product,
            0
        )

        popularity = popular_scores.get(
            product,
            0
        )

        hybrid_scores[product] = (
            0.3 * content
            +
            0.5 * collab
            +
            0.2 * popularity
        )

    final_recommendations = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for product, score in final_recommendations[:top_n]:

        details = get_product_details(
            product
        )

        reasons = generate_reason(
            product,
            content_scores,
            collab_scores,
            popular_scores
        )

        results.append(
            {
                "product_id": details["product_id"],
                "brand": details["brand"],
                "category": details["category"],
                "price": details["price"],
                "score": round(score, 4),
                "reasons": reasons
            }
        )

    return results


# Testing
if __name__ == "__main__":

    recommendations = (
        get_hybrid_recommendations(
            1004856
        )
    )

    print("\nHybrid Recommendations:\n")

    for item in recommendations:

        print("\n------------------------")

        print(
            f"Product ID: {item['product_id']}"
        )

        print(
            f"Brand: {item['brand']}"
        )

        print(
            f"Category: {item['category']}"
        )

        print(
            f"Price: {item['price']}"
        )

        print("\nReason:")

        for reason in item["reasons"]:
            print(f"✓ {reason}")

        print(
            f"\nHybrid Score: {item['score']}"
        )