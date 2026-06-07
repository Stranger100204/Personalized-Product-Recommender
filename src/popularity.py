import pandas as pd

# Load dataset once
df = pd.read_csv(
    "data/2019-Oct.csv",
    nrows=500000
)

def get_popular_products(top_n=10):

    popular = (
        df[df["event_type"] == "purchase"]
        .groupby("product_id")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
    )

    return popular.to_dict()


# Testing
if __name__ == "__main__":

    popular = get_popular_products()

    print("\nPopular Products:\n")

    for product, score in popular.items():
        print(
            f"Product: {product} | Purchases: {score}"
        )