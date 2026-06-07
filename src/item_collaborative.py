import pandas as pd

# Load interactions once
df = pd.read_csv("data/user_product_interactions.csv")

# Active users
active_users = (
    df.groupby("user_id")
      .size()
      .loc[lambda x: x >= 3]
      .index
)

df = df[df["user_id"].isin(active_users)]

# Popular products
popular_products = (
    df.groupby("product_id")
      .size()
      .loc[lambda x: x >= 5]
      .index
)

df = df[df["product_id"].isin(popular_products)]


def get_collaborative_recommendations(product_id, top_n=5):

    if product_id not in df["product_id"].values:
        return []

    users_who_interacted = set(
        df[df["product_id"] == product_id]["user_id"]
    )

    similar_products = {}

    for product in df["product_id"].unique():

        if product == product_id:
            continue

        users_for_product = set(
            df[df["product_id"] == product]["user_id"]
        )

        overlap = len(
            users_who_interacted.intersection(users_for_product)
        )

        if overlap > 0:
            similar_products[product] = overlap

    recommendations = sorted(
        similar_products.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return [product for product, score in recommendations]


# Testing
if __name__ == "__main__":

    recs = get_collaborative_recommendations(
        1004856
    )

    print("\nCollaborative Recommendations:\n")

    for r in recs:
        print(r)