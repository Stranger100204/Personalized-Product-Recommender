from content_based import get_content_recommendations
from item_collaborative import get_collaborative_recommendations
from popularity import get_popular_products

product_id = 1004856

print("Generating Hybrid Recommendations...\n")

# Get recommendations
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

# Combine all products
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

# Sort recommendations
final_recommendations = sorted(
    hybrid_scores.items(),
    key=lambda x: x[1],
    reverse=True
)

print("Top Hybrid Recommendations:\n")

for product, score in final_recommendations[:10]:

    print(
        f"Product: {product} | Hybrid Score: {score:.4f}"
    )