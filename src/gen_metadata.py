import pandas as pd
from metadata_templates import (
    NAME_SUFFIX,
    DESCRIPTION_TEMPLATE
)


# -----------------------------
# Load Original Catalog
# -----------------------------
catalog = pd.read_csv("data/product_catalog.csv")

catalog["brand"] = catalog["brand"].fillna("Unknown")
catalog["category_code"] = catalog["category_code"].fillna("Misc.Product")


# -----------------------------
# Category Parser
# -----------------------------
def parse_category(cat_code):

    parts = str(cat_code).split(".")

    category = parts[0].replace("_", " ").title()

    subcategory = parts[-1].replace("_", " ").title()

    return category, subcategory


catalog[["category", "subcategory"]] = catalog["category_code"].apply(
    lambda x: pd.Series(parse_category(x))
)


# -----------------------------
# Price Bucket
# -----------------------------
def get_price_bucket(price):

    if price < 100:
        return "Budget"

    elif price < 500:
        return "Mid-Range"

    elif price < 1000:
        return "Premium"

    else:
        return "Luxury"


catalog["price_bucket"] = catalog["price"].apply(
    get_price_bucket
)


# -----------------------------
# Product Name Generator
# -----------------------------
def generate_product_name(row):

    brand = row["brand"].title()

    sub = row["subcategory"].lower().replace(" ", "_")

    product = NAME_SUFFIX.get(
        sub,
        NAME_SUFFIX["default"]
    )

    if brand == "Unknown":
        return product

    return f"{brand} {product}"


catalog["product_name"] = catalog.apply(
    generate_product_name,
    axis=1
)


# -----------------------------
# Description Generator
# -----------------------------
def generate_description(row):

    template = DESCRIPTION_TEMPLATE.get(
        row["category"],
        DESCRIPTION_TEMPLATE["Default"]
    )

    return template.format(

        brand=row["brand"].title(),

        name=row["product_name"]

    )


catalog["description"] = catalog.apply(
    generate_description,
    axis=1
)


# -----------------------------
# Search Text
# -----------------------------
catalog["search_text"] = (

    catalog["product_name"]

    + " "

    + catalog["category"]

    + " "

    + catalog["subcategory"]

    + " "

    + catalog["price_bucket"]

    + " "

    + catalog["description"]

)


# -----------------------------
# Save Metadata
# -----------------------------
metadata = catalog[
    [
        "product_id",
        "product_name",
        "brand",
        "category",
        "subcategory",
        "price",
        "price_bucket",
        "description",
        "search_text",
    ]
]

metadata.to_csv(
    "data/product_metadata.csv",
    index=False
)

print("\nMetadata Generated Successfully!\n")

print(metadata.head())

print("\nCategories :", metadata["category"].nunique())
print("Brands     :", metadata["brand"].nunique())
print("Products   :", len(metadata))