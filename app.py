import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="US Top 50 Playlist Analytics",
    layout="wide"
)

# ==================================================
# FILE PATH
# ==================================================
from pathlib import Path

BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "Atlantic_United_States.csv"

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv(FILE_PATH, sep="\t")

    df.columns = df.columns.str.strip()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["duration_min"] = df["duration_ms"] / 60000

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ==================================================
# TITLE
# ==================================================
st.title("🎵 US Top 50 Playlist Analytics Dashboard")
st.success(f"Loaded {len(df):,} records")

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.header("Filters")

artist_filter = st.sidebar.multiselect(
    "Artist",
    sorted(df["artist"].dropna().unique())
)

if artist_filter:
    df = df[df["artist"].isin(artist_filter)]

# ==================================================
# KPI CARDS
# ==================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Songs", df["song"].nunique())
col2.metric("Artists", df["artist"].nunique())
col3.metric("Avg Popularity", round(df["popularity"].mean(), 1))
col4.metric(
    "Explicit %",
    round(df["is_explicit"].mean() * 100, 1)
)

# ==================================================
# RANK DISTRIBUTION
# ==================================================
st.subheader("📊 Rank Distribution")

fig = px.histogram(
    df,
    x="position",
    nbins=25,
    title="Playlist Rank Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="rank_distribution"
)

# ==================================================
# POPULARITY VS POSITION
# ==================================================
st.subheader("🎯 Popularity vs Position")

fig = px.scatter(
    df,
    x="position",
    y="popularity",
    color="album_type",
    hover_data=["song", "artist"]
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="popularity_position"
)

# ==================================================
# DAILY PLAYLIST ACTIVITY
# ==================================================
st.subheader("📈 Daily Playlist Activity")

daily_songs = (
    df.groupby("date")["song"]
      .count()
      .reset_index()
)

fig = px.line(
    daily_songs,
    x="date",
    y="song",
    title="Daily Playlist Activity"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="daily_activity"
)

# ==================================================
# TOP 10 MOST POPULAR SONGS
# ==================================================
st.subheader("🔥 Top 10 Most Popular Songs")

top_popular = (
    df.groupby("song")["popularity"]
      .mean()
      .sort_values(ascending=False)
      .head(10)
)

fig = px.bar(
    x=top_popular.values,
    y=top_popular.index,
    orientation="h",
    title="Top 10 Most Popular Songs"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="top_songs"
)

# ==================================================
# ARTIST DOMINANCE
# ==================================================
st.subheader("🎤 Artist Dominance")

artist_days = (
    df.groupby("artist")["date"]
      .count()
      .sort_values(ascending=False)
      .head(10)
)

fig = px.bar(
    x=artist_days.index,
    y=artist_days.values,
    title="Top Artists by Playlist Appearances"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="artist_dominance"
)

# ==================================================
# TOP ARTISTS BY POPULARITY
# ==================================================
st.subheader("⭐ Top Artists by Average Popularity")

artist_pop = (
    df.groupby("artist")["popularity"]
      .mean()
      .sort_values(ascending=False)
      .head(10)
)

fig = px.bar(
    x=artist_pop.values,
    y=artist_pop.index,
    orientation="h",
    title="Top Artists by Average Popularity"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="artist_popularity"
)

# ==================================================
# SONG LONGEVITY ANALYSIS
# ==================================================
st.subheader("⏳ Song Longevity Analysis")

song_days = (
    df.groupby("song")["date"]
      .nunique()
      .sort_values(ascending=False)
      .head(15)
)

fig = px.bar(
    x=song_days.values,
    y=song_days.index,
    orientation="h",
    title="Songs with Longest Playlist Presence"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="song_longevity"
)

# ==================================================
# ALBUM TYPE DISTRIBUTION
# ==================================================
st.subheader("💿 Album Type Distribution")

fig = px.pie(
    df,
    names="album_type",
    title="Album Type Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="album_distribution"
)

# ==================================================
# EXPLICIT VS NON-EXPLICIT
# ==================================================
st.subheader("🚫 Explicit vs Non-Explicit Analysis")

explicit = (
    df.groupby("is_explicit")["popularity"]
      .mean()
      .reset_index()
)

fig = px.bar(
    explicit,
    x="is_explicit",
    y="popularity",
    title="Average Popularity by Explicit Content"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="explicit_analysis"
)

# ==================================================
# DURATION VS POPULARITY
# ==================================================
st.subheader("⏱ Duration vs Popularity")

fig = px.scatter(
    df,
    x="duration_min",
    y="popularity",
    color="album_type",
    hover_data=["song", "artist"]
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="duration_popularity"
)

# ==================================================
# DATASET PREVIEW
# ==================================================
st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(100),
    use_container_width=True
)