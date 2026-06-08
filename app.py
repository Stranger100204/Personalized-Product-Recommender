import streamlit as st

from src.hybrid import get_hybrid_recommendations
from src.explainability import get_product_details

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

product_id = st.number_input(
    "Enter Product ID",
    value=1004856,
    step=1
)

if st.button("Get Recommendations"):

    selected_product = get_product_details(
        int(product_id)
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
        int(product_id)
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