import pandas as pd


class ProductSearch:

    def __init__(self):

        self.products = pd.read_csv(
            "data/product_metadata.csv"
        )

        self.products["brand"] = (
            self.products["brand"]
            .fillna("")
            .str.lower()
        )

        self.products["product_name"] = (
            self.products["product_name"]
            .fillna("")
            .str.lower()
        )

        self.products["category"] = (
            self.products["category"]
            .fillna("")
            .str.lower()
        )


    def search_by_id(self, product_id):

        return self.products[
            self.products["product_id"] == product_id
        ]


    def search_by_brand(self, brand):

        brand = brand.lower()

        return self.products[

            self.products["brand"].str.contains(
                brand,
                case=False,
                na=False
            )

        ]


    def search_by_name(self, name):

        name = name.lower()

        return self.products[

            self.products["product_name"].str.contains(
                name,
                case=False,
                na=False
            )

        ]


    def search_products(self, query):

        query = str(query).strip()

        if query.isdigit():

            results = self.search_by_id(
                int(query)
            )

            if not results.empty:
                return results

        results = self.search_by_name(query)

        if not results.empty:
            return results

        results = self.search_by_brand(query)

        return results