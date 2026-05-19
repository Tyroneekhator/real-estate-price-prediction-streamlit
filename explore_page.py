import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rcParams["figure.figsize"] = (10, 6)


def outliers(df, ft):
    q1 = df[ft].quantile(0.25)
    q3 = df[ft].quantile(0.75)
    iqr = q3 - q1
    min_val = q1 - 1.5 * iqr
    max_val = q3 + 1.5 * iqr
    return df.index[(df[ft] < min_val) | (df[ft] > max_val)]


def remove(df, indices):
    indices = sorted(set(indices))
    return df.drop(indices)


def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for _, subdf in df.groupby("state"):
        mean_val = np.mean(subdf.price_per_room)
        std_val = np.std(subdf.price_per_room)
        reduced_df = subdf[
            (subdf.price_per_room > (mean_val - std_val))
            & (subdf.price_per_room <= (mean_val + std_val))
        ]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out


@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("nigeria_houses_data.csv")

    if "toilets" in df.columns:
        df = df.drop(["toilets"], axis=1)

    index_list = []
    for col in ["bedrooms", "bathrooms", "parking_space", "price"]:
        if col in df.columns:
            index_list.extend(outliers(df, col))

    df2 = remove(df, index_list).copy()

    if "title" in df2.columns:
        df2 = df2.rename(columns={"title": "house_type"})

    df2["total_rooms"] = df2["bedrooms"] + df2["bathrooms"]
    df2["price_per_room"] = df2["price"] / df2["total_rooms"].replace(0, np.nan)
    df2 = df2.dropna().copy()

    df3 = remove_pps_outliers(df2).copy()

    few_state_records = df3["state"].value_counts()
    few_town_records = df3["town"].value_counts()

    df4 = df3[
        ~df3["state"].isin(few_state_records[few_state_records < 10].index)
        & ~df3["town"].isin(few_town_records[few_town_records < 10].index)
    ].copy()

    if "parking_space" in df4.columns:
        df4 = df4.drop(["parking_space"], axis=1)

    return df4


def metric_card(label, value, subtext):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_explore_page():
    df4 = load_and_clean_data()

    st.markdown(
        """
        <div class="app-hero">
            <h1 style="margin:0 0 8px 0;">Market Insights</h1>
            <p class="small-muted" style="margin:0;">
                Explore housing price trends across Nigerian states, towns, and property types.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    avg_price = df4["price"].mean()
    top_state = df4.groupby("state")["price"].mean().sort_values(ascending=False).index[0]
    top_town = df4.groupby("town")["price"].mean().sort_values(ascending=False).index[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Properties", f"{len(df4):,}", "Cleaned records analyzed")
    with c2:
        metric_card("Average Price", f"₦{avg_price:,.0f}", "Mean listing price")
    with c3:
        metric_card("Top State", top_state, "Highest average price")
    with c4:
        metric_card("Top Town", top_town, "Most expensive market")

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Most Expensive Towns</div>', unsafe_allow_html=True)

        fig, ax = plt.subplots()
        (
            df4.groupby("town")["price"].mean().sort_values(ascending=False).head(20) / 1e6
        ).plot(kind="bar", ax=ax)
        ax.set_xlabel("Town")
        ax.set_ylabel("Average Price [₦1M]")
        ax.set_title("Top 20 Most Expensive Real Estate Towns")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Average Price by State</div>', unsafe_allow_html=True)

        fig, ax = plt.subplots()
        (
            df4.groupby("state")["price"].mean().sort_values(ascending=False) / 1e6
        ).plot(kind="bar", ax=ax)
        ax.set_xlabel("State")
        ax.set_ylabel("Average Price [₦1M]")
        ax.set_title("Average House Price by State")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Average Price by House Type</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots()
    (
        df4.groupby("house_type")["price"].mean().sort_values(ascending=False) / 1e6
    ).plot(kind="barh", ax=ax)
    ax.set_xlabel("Average Price [₦1M]")
    ax.set_ylabel("House Type")
    ax.set_title("Average Price by Property Type")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Price vs Price Per Room</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.scatterplot(
        data=df4,
        hue="house_type",
        x=df4["price_per_room"] / 1e6,
        y=df4["price"] / 1e6,
        ax=ax,
    )
    ax.set_xlabel("Price Per Room [₦1M]")
    ax.set_ylabel("Price [₦1M]")
    ax.set_title("Relationship Between Price and Price Per Room")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)
