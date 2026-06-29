import streamlit as st

from src.hybrid import get_hybrid_recommendations
from src.explainability import get_product_details
from src.search import ProductSearch

search_engine = ProductSearch()

st.title("🛒 Personalized Product Recommendation System")

st.markdown(
    """
    Discover personalized product recommendations using a hybrid recommendation engine that combines
    content-based filtering, collaborative filtering, and popularity-based ranking.
    """
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Products",
    "46,897"
)

col2.metric(
    "Users",
    "89,124"
)

col3.metric(
    "Interactions",
    "314,804"
)

query = st.text_input(
    "🔍 Search Product",
    placeholder="Search by Product ID, Brand or Product Name..."
)

selected_product_id = None

if query:

    results = search_engine.search_products(query)

    if results.empty:

        st.warning("No matching products found.")

    else:

        options = {}

        for _, row in results.iterrows():

            label = (
                f"{row['product_name']} | "
                f"{row['brand'].title()} | "
                f"{row['category'].title()} | "
                f"${row['price']:.2f}"
            )

            options[label] = row["product_id"]

        selected = st.selectbox(
            "Select Product",
            list(options.keys())
        )

        selected_product_id = options[selected]

if st.button("Get Recommendations"):

    if selected_product_id is None:

        st.error(
            "Please search and select a product first."
        )

        st.stop()

    selected_product = get_product_details(
        selected_product_id
    )

    st.subheader("Selected Product")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Product ID:** {selected_product['product_id']}"
        )

        st.write(
            f"**Brand:** {selected_product['brand']}"
        )

    with col2:

        st.write(
            f"**Category:** {selected_product['category']}"
        )

        st.write(
            f"**Price:** ${selected_product['price']}"
        )

    st.divider()

    st.subheader("🏆 Top Recommended Products")

    st.caption(
        "Ranked using a hybrid score combining collaborative, content-based, and popularity signals."
    )

    recommendations = get_hybrid_recommendations(
        selected_product_id
    )

    if not recommendations:

        st.error(
            "Product not found in recommendation database."
        )

        st.stop()

    for rank, item in enumerate(
        recommendations,
        start=1
    ):

        with st.container():

            if rank == 1:
                badge = "🥇"

            elif rank == 2:
                badge = "🥈"

            elif rank == 3:
                badge = "🥉"

            else:
                badge = "🏆"

            st.subheader(
                f"{badge} #{rank} Product {item['product_id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"Brand: {item['brand']}"
                )

                st.write(
                    f"Category: {item['category']}"
                )

            with col2:
                st.write(
                    f"Price: ${item['price']}"
                )

                st.write(
                    f"Hybrid Score: {item['score']:.4f}"
                )

            st.write("Reasons:")

            for reason in item["reasons"]:
                st.success(reason)

            st.divider()

with st.sidebar:

    st.title("About")

    st.write(
        """
        Hybrid Recommendation Engine

        • Content-Based Filtering

        • Collaborative Filtering

        • Popularity-Based Ranking

        • Explainable Recommendations
        """
    )