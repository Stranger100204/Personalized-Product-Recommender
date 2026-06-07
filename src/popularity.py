import pandas as pd

# Load dataset once
df = pd.read_csv(
    "data/2019-Oct.csv",
    nrows=500000
)


def get_popular_products(top_n=10):

    top_products = (
        df[df["event_type"] == "purchase"]
        .groupby("product_id")
        .size()
        .sort_values(ascending=False)
        .head(top_n)
        .index
        .tolist()
    )

    return top_products


# Testing
if __name__ == "__main__":

    popular = get_popular_products()

    print("\nPopular Products:\n")

    for product in popular:
        print(product)