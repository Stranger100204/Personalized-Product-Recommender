import pandas as pd

print("Loading dataset...")

df = pd.read_csv(
    "data/2019-Oct.csv",
    nrows=500000
)

# Convert datetime
df["event_time"] = pd.to_datetime(df["event_time"])

# Fill missing values
df["brand"] = df["brand"].fillna("Unknown_Brand")
df["category_code"] = df["category_code"].fillna("Unknown_Category")

# Interaction weights
weights = {
    "view": 1,
    "cart": 3,
    "purchase": 5
}

df["interaction_score"] = df["event_type"].map(weights)

print("\nInteraction Distribution:")
print(df["interaction_score"].value_counts())

# Aggregate user-product interactions
interaction_df = (
    df.groupby(["user_id", "product_id"])
      ["interaction_score"]
      .sum()
      .reset_index()
)

print("\nInteraction Matrix Shape:")
print(interaction_df.shape)

print("\nTop Interactions:")
print(interaction_df.head())

interaction_df.to_csv(
    "data/user_product_interactions.csv",
    index=False
)

print("\nSaved successfully.")