import pandas as pd

df = pd.read_csv(
    "data/2019-Oct.csv",
    nrows=500000
)

catalog = (
    df[
        ["product_id", "category_code", "brand", "price"]
    ]
    .drop_duplicates("product_id")
)

print(catalog.head())

print("\nProducts:")
print(len(catalog))

catalog.to_csv(
    "data/product_catalog.csv",
    index=False
)

print("\nCatalog Saved")