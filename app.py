import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.hybrid import get_hybrid_recommendations
from src.explainability import get_product_details
from src.search import ProductSearch

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopMind — Personalized Recommender",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* Hero title */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Product cards */
    .product-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 0.6rem;
        transition: border-color 0.2s;
    }

    .product-card:hover {
        border-color: rgba(167,139,250,0.5);
    }

    .product-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: #e2e8f0;
        margin-bottom: 0.25rem;
    }

    .product-meta {
        font-size: 0.82rem;
        color: #cbd5e1;
    }

    /* Price bucket badges */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-top: 4px;
    }
    .badge-budget    { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid #34d399; }
    .badge-midrange  { background: rgba(96,165,250,0.15); color: #60a5fa; border: 1px solid #60a5fa; }
    .badge-premium   { background: rgba(251,146,60,0.15);  color: #fb923c; border: 1px solid #fb923c; }
    .badge-luxury    { background: rgba(192,132,252,0.15); color: #c084fc; border: 1px solid #c084fc; }
    .badge-unknown   { background: rgba(148,163,184,0.15); color: #94a3b8; border: 1px solid #94a3b8; }

    /* Recommendation cards */
    .rec-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .rec-rank {
        font-size: 1.4rem;
        margin-right: 0.4rem;
    }

    .rec-title {
        font-size: 1rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    .reason-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin: 2px 4px 2px 0;
        background: rgba(167,139,250,0.15);
        color: #a78bfa;
        border: 1px solid rgba(167,139,250,0.4);
    }

    /* Selected product panel */
    .selected-panel {
        background: linear-gradient(135deg, rgba(96,165,250,0.1), rgba(167,139,250,0.08));
        border: 1px solid rgba(96,165,250,0.3);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
    }

    /* Section dividers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 1.5rem 0 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 0.8rem 1rem;
    }

    /* Force metric label and value to be bright */
    [data-testid="stMetricLabel"] > div {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] > div {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    /* Make all regular text visible */
    p, span, div, label {
        color: #e2e8f0;
    }

    /* Expander text */
    [data-testid="stExpander"] summary {
        color: #f1f5f9 !important;
        font-weight: 600;
    }

    /* Hide Streamlit default header decoration */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Match Streamlit top toolbar to dark background */
    [data-testid="stHeader"],
    .stAppHeader,
    header {
        background-color: #0f0c29 !important;
        background: #0f0c29 !important;
    }

    /* Make toolbar buttons/text visible */
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] a,
    [data-testid="stHeader"] span,
    .stAppHeader button,
    .stAppHeader span {
        color: #cbd5e1 !important;
    }

    /* Select / secondary buttons — dark text on white bg */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #d1d5db !important;
        font-weight: 700 !important;
    }

    div.stButton > button:hover {
        background-color: #f3f4f6 !important;
        border-color: #9ca3af !important;
        color: #000000 !important;
    }
    
    div.stButton > button p {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ── Cached data & engine ────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="🔍 Building semantic search index…")
def load_search_engine():
    return ProductSearch()


@st.cache_data(show_spinner=False)
def load_catalog():
    return pd.read_csv("data/product_catalog.csv")


@st.cache_data(show_spinner=False)
def load_metadata():
    return pd.read_csv("data/product_metadata.csv")


@st.cache_data(show_spinner=False)
def load_interactions():
    return pd.read_csv("data/user_product_interactions.csv")


@st.cache_data(show_spinner=False)
def load_events(nrows=500_000):
    return pd.read_csv("data/2019-Oct.csv", nrows=nrows)


search_engine = load_search_engine()

# ── Sidebar ─────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        "<h2 style='color:#a78bfa; margin-bottom:0.2rem;'>🛒 ShopMind</h2>"
        "<p style='color:#cbd5e1; font-size:0.8rem; margin-top:0;'>Hybrid Recommendation Engine</p>",
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
        ["🔍 Search & Recommend", "📊 Analytics"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        "<p style='color:#cbd5e1; font-size:0.78rem;'>"
        "Powered by<br>"
        "• Content-Based Filtering (30%)<br>"
        "• Collaborative Filtering (50%)<br>"
        "• Popularity Ranking (20%)"
        "</p>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — SEARCH & RECOMMEND
# ══════════════════════════════════════════════════════════════════════════════

def _price_bucket_badge(bucket: str) -> str:
    mapping = {
        "Budget":    "badge-budget",
        "Mid-Range": "badge-midrange",
        "Premium":   "badge-premium",
        "Luxury":    "badge-luxury",
    }
    css = mapping.get(bucket, "badge-unknown")
    return f'<span class="badge {css}">{bucket}</span>'


def _rank_icon(rank: int) -> str:
    icons = {1: "🥇", 2: "🥈", 3: "🥉"}
    return icons.get(rank, f"#{rank}")


def page_search():

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="hero-title">Personalized Product Recommendations</div>'
        '<div class="hero-subtitle">Discover products tailored to your interests using AI-powered hybrid recommendations.</div>',
        unsafe_allow_html=True
    )

    # ── Stats row ──────────────────────────────────────────────────────────────
    catalog = load_catalog()
    interactions = load_interactions()
    metadata = load_metadata()

    col1, col2, col3 = st.columns(3)
    col1.metric("🛍️ Products", f"{len(metadata):,}")
    col2.metric("👥 Users", f"{interactions['user_id'].nunique():,}")
    col3.metric("⚡ Interactions", f"{len(interactions):,}")

    st.markdown("---")

    # ── Search bar ─────────────────────────────────────────────────────────────
    query = st.text_input(
        "🔍 Search Product",
        placeholder='Try "gaming laptop", "wireless earphones", "budget smartphone"…',
        key="search_query"
    )

    # ── Search results as product cards ────────────────────────────────────────
    if query:

        with st.spinner("Searching…"):
            results = search_engine.search_products(query, top_k=10)

        if results.empty:
            st.warning("⚠️ No matching products found. Try a different query.")

        else:
            st.markdown(
                f'<div class="section-header">Search Results '
                f'<span style="color:#94a3b8;font-size:0.85rem;font-weight:400;">({len(results)} products found)</span></div>',
                unsafe_allow_html=True
            )

            # Render each result as a card + select button
            for _, row in results.iterrows():

                pid = int(row["product_id"])
                bucket = str(row.get("price_bucket", "Unknown"))
                badge_html = _price_bucket_badge(bucket)

                with st.container():
                    card_col, btn_col = st.columns([5, 1])

                    with card_col:
                        st.markdown(
                            f'<div class="product-card">'
                            f'<div class="product-title">{row["product_name"].title()}</div>'
                            f'<div class="product-meta">'
                            f'🏷️ {str(row["brand"]).title()} &nbsp;|&nbsp; '
                            f'📂 {str(row["category"]).title()} &nbsp;|&nbsp; '
                            f'💰 ${float(row["price"]):.2f}'
                            f'</div>'
                            f'{badge_html}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    with btn_col:
                        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
                        if st.button("Select", key=f"select_{pid}"):
                            st.session_state["selected_product_id"] = pid
                            st.session_state["selected_product_row"] = row.to_dict()
                            st.rerun()

    # ── Selected product panel ─────────────────────────────────────────────────
    selected_id = st.session_state.get("selected_product_id")
    selected_row = st.session_state.get("selected_product_row")

    if selected_id and selected_row:

        st.markdown(
            '<div class="section-header">Selected Product</div>',
            unsafe_allow_html=True
        )

        bucket = str(selected_row.get("price_bucket", "Unknown"))
        badge_html = _price_bucket_badge(bucket)

        st.markdown(
            f'<div class="selected-panel">'
            f'<div class="product-title" style="font-size:1.05rem;">'
            f'{str(selected_row.get("product_name", "")).title()}</div>'
            f'<div class="product-meta" style="margin-top:6px;">'
            f'🏷️ <b>{str(selected_row.get("brand","")).title()}</b> &nbsp;|&nbsp; '
            f'📂 {str(selected_row.get("category","")).title()} &nbsp;|&nbsp; '
            f'💰 <b>${float(selected_row.get("price", 0)):.2f}</b>'
            f'</div>'
            f'<div style="margin-top:6px;">{badge_html}</div>'
            f'<div class="product-meta" style="margin-top:6px; color:#94a3b8;">'
            f'Product ID: {selected_id}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── Recommend button ──────────────────────────────────────────────────
        if st.button("Get Recommendations", type="primary", use_container_width=True):

            with st.spinner("🤖 Computing hybrid recommendations…"):
                recommendations = get_hybrid_recommendations(selected_id)

            if not recommendations:
                st.error("❌ Product not found in recommendation database.")
                st.stop()

            st.markdown(
                '<div class="section-header">🏆 Top Recommended Products</div>',
                unsafe_allow_html=True
            )
            st.caption(
                "Ranked by a weighted hybrid score: 50% Collaborative · 30% Content · 20% Popularity"
            )

            for rank, item in enumerate(recommendations, start=1):

                rank_icon = _rank_icon(rank)
                bucket = item.get("price_bucket", "Unknown")
                badge_html = _price_bucket_badge(bucket)

                # Reason badges HTML
                reasons_html = "".join(
                    f'<span class="reason-badge">{r}</span>'
                    for r in item["reasons"]
                )

                st.markdown(
                    f'<div class="rec-card">'
                    f'<span class="rec-rank">{rank_icon}</span>'
                    f'<span class="rec-title">{str(item["product_name"]).title()}</span>'
                    f'<div class="product-meta" style="margin-top:6px;">'
                    f'🏷️ {str(item["brand"]).title()} &nbsp;|&nbsp; '
                    f'📂 {str(item["category"]).title()} &nbsp;|&nbsp; '
                    f'💰 ${float(item["price"]):.2f} &nbsp;'
                    f'{badge_html}'
                    f'</div>'
                    f'<div style="margin-top:8px;">{reasons_html}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Score breakdown using Streamlit native widgets
                with st.expander(f"📊 Score Breakdown — #{rank} {str(item['product_name']).title()[:40]}"):

                    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
                    s_col1.metric("🤝 Collaborative", f"{item['collaborative_score']:.3f}")
                    s_col2.metric("🔍 Content", f"{item['content_score']:.3f}")
                    s_col3.metric("🔥 Popularity", f"{item['popularity_score']:.3f}")
                    s_col4.metric("⭐ Hybrid", f"{item['score']:.4f}")

                    st.markdown("**Collaborative (50%)**")
                    st.progress(float(item["collaborative_score"]))

                    st.markdown("**Content-Based (30%)**")
                    st.progress(float(item["content_score"]))

                    st.markdown("**Popularity (20%)**")
                    st.progress(float(item["popularity_score"]))

                    st.markdown("**Overall Hybrid Score**")
                    st.progress(float(item["score"]))


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — ANALYTICS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

PLOTLY_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(15,12,41,0.6)",
    "font": {"family": "Inter", "color": "#f1f5f9", "size": 13},
    "xaxis": {
        "gridcolor": "rgba(255,255,255,0.08)",
        "linecolor": "rgba(255,255,255,0.15)",
        "tickfont": {"color": "#e2e8f0"},
        "title_font": {"color": "#f1f5f9"},
    },
    "yaxis": {
        "gridcolor": "rgba(255,255,255,0.08)",
        "linecolor": "rgba(255,255,255,0.15)",
        "tickfont": {"color": "#e2e8f0"},
        "title_font": {"color": "#f1f5f9"},
    },
    "margin": {"t": 50, "b": 40, "l": 10, "r": 80},
}


def page_analytics():

    st.markdown(
        '<div class="hero-title">📊 Analytics Dashboard</div>'
        '<div class="hero-subtitle">Insights from the product catalog and user interaction data.</div>',
        unsafe_allow_html=True
    )

    with st.spinner("Loading analytics data…"):
        catalog = load_catalog()
        metadata = load_metadata()
        interactions = load_interactions()
        events = load_events()

    # ── Catalog stats ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">📈 Catalog Overview</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🛍️ Total Products", f"{len(metadata):,}")
    m2.metric("👥 Total Users", f"{interactions['user_id'].nunique():,}")
    m3.metric("⚡ Total Interactions", f"{len(interactions):,}")
    m4.metric("📂 Categories", f"{catalog['category_code'].nunique():,}")

    st.markdown("---")

    # ── Row 1: Top brands | Category distribution ─────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">🏷️ Top 10 Popular Brands</div>', unsafe_allow_html=True)

        # Join interactions with catalog to get brand per product
        brand_interactions = (
            interactions
            .merge(
                catalog[["product_id", "brand"]].drop_duplicates(),
                on="product_id",
                how="left"
            )
            .dropna(subset=["brand"])
        )

        top_brands = (
            brand_interactions
            .groupby("brand")["interaction_score"]
            .sum()
            .sort_values(ascending=True)
            .tail(10)
        )

        fig_brands = go.Figure(
            go.Bar(
                x=top_brands.values,
                y=top_brands.index.str.title(),
                orientation="h",
                marker=dict(
                    color=top_brands.values,
                    colorscale="Purp",
                    showscale=False,
                ),
                text=[f"{int(v):,}" for v in top_brands.values],
                textposition="outside",
                textfont=dict(color="#f1f5f9", size=12),
            )
        )
        fig_brands.update_layout(
            **PLOTLY_THEME,
            height=380,
            xaxis_title="Total Interaction Score",
            yaxis_title="",
        )
        st.plotly_chart(fig_brands, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">📂 Category Distribution</div>', unsafe_allow_html=True)

        top_categories = (
            catalog["category_code"]
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
        )

        fig_cat = go.Figure(
            go.Bar(
                x=top_categories.values,
                y=top_categories.index.str.title(),
                orientation="h",
                marker=dict(
                    color=top_categories.values,
                    colorscale="Blues",
                    showscale=False,
                ),
                text=[f"{int(v):,}" for v in top_categories.values],
                textposition="outside",
                textfont=dict(color="#f1f5f9", size=12),
            )
        )
        fig_cat.update_layout(
            **PLOTLY_THEME,
            height=380,
            xaxis_title="Product Count",
            yaxis_title="",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # ── Row 2: Price distribution | Price bucket breakdown ────────────────────
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.markdown('<div class="section-header">💰 Price Distribution</div>', unsafe_allow_html=True)

        prices = catalog["price"].dropna()
        prices = prices[prices < prices.quantile(0.99)]  # trim outliers

        fig_price = px.histogram(
            prices,
            nbins=50,
            labels={"value": "Price ($)", "count": "Products"},
            color_discrete_sequence=["#a78bfa"],
        )
        fig_price.update_traces(
            marker_line_color="rgba(0,0,0,0.3)",
            marker_line_width=0.5,
            opacity=0.85,
        )
        fig_price.update_layout(
            **PLOTLY_THEME,
            height=340,
            xaxis_title="Price ($)",
            yaxis_title="Number of Products",
            showlegend=False,
        )
        st.plotly_chart(fig_price, use_container_width=True)

    with col_right2:
        st.markdown('<div class="section-header">🎯 Price Bucket Breakdown</div>', unsafe_allow_html=True)

        bucket_colors = {
            "Budget": "#34d399",
            "Mid-Range": "#60a5fa",
            "Premium": "#fb923c",
            "Luxury": "#c084fc",
        }

        bucket_counts = metadata["price_bucket"].value_counts()

        fig_bucket = go.Figure(
            go.Pie(
                labels=bucket_counts.index,
                values=bucket_counts.values,
                hole=0.55,
                marker=dict(
                    colors=[
                        bucket_colors.get(label, "#94a3b8")
                        for label in bucket_counts.index
                    ],
                    line=dict(color="rgba(0,0,0,0.2)", width=2),
                ),
                textinfo="label+percent",
                textfont=dict(color="#ffffff", size=13),
            )
        )
        fig_bucket.update_layout(
            **PLOTLY_THEME,
            height=340,
            showlegend=True,
            legend=dict(
                orientation="v",
                font=dict(color="#f1f5f9", size=12),
            ),
        )
        st.plotly_chart(fig_bucket, use_container_width=True)

    st.markdown("---")

    # ── Top trending products ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔥 Top 10 Trending Products</div>', unsafe_allow_html=True)

    purchase_events = events[events["event_type"] == "purchase"]
    top_purchases = (
        purchase_events
        .groupby("product_id")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .rename(columns={0: "purchases"})
    )

    # Merge with metadata for product names
    top_purchases = top_purchases.merge(
        metadata[["product_id", "product_name", "brand"]].drop_duplicates(),
        on="product_id",
        how="left"
    )
    top_purchases["label"] = (
        top_purchases["product_name"]
        .fillna(top_purchases["product_id"].astype(str))
        .str.title()
        .str[:35]
        + " (" + top_purchases["brand"].fillna("").str.title() + ")"
    )
    top_purchases = top_purchases.sort_values("purchases", ascending=True)

    fig_trending = go.Figure(
        go.Bar(
            x=top_purchases["purchases"],
            y=top_purchases["label"],
            orientation="h",
            marker=dict(
                color=top_purchases["purchases"],
                colorscale="Teal",
                showscale=False,
            ),
            text=[f"{int(v):,}" for v in top_purchases["purchases"]],
            textposition="outside",
            textfont=dict(color="#f1f5f9", size=12),
        )
    )
    fig_trending.update_layout(
        **PLOTLY_THEME,
        height=400,
        xaxis_title="Purchase Count",
        yaxis_title="",
    )
    st.plotly_chart(fig_trending, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if page == "🔍 Search & Recommend":
    page_search()
else:
    page_analytics()