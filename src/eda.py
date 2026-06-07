import pandas as pd

# Load sample only
df = pd.read_csv(
    "data/2019-Oct.csv",
    nrows=500000
)

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nEvent Types:")
print(df["event_type"].value_counts())

print("\nUnique Users:")
print(df["user_id"].nunique())

print("\nUnique Products:")
print(df["product_id"].nunique())