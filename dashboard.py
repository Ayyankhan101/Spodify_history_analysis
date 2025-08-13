"""
Spotify History Analysis Dashboard
---------------------------------
A Streamlit app to explore your personal Spotify listening history.
"""

from __future__ import annotations
import altair as alt
import pandas as pd
import streamlit as st
from pathlib import Path

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Spotify History Analysis",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

alt.themes.enable("dark")

# ---------- CONSTANTS ----------
CSV_PATH = Path("spotify_history.csv")
DATE_COL = "ts"
REQUIRED_COLS = {
    "ts",
    "artist_name",
    "album_name",
    "track_name",
    "ms_played",
    "platform",
}

# ---------- CACHING ----------
@st.cache_data(show_spinner="Loading & filtering dataset …")
def load_data(path: Path) -> pd.DataFrame | None:
    """Load and preprocess the raw CSV."""
    if not path.exists():
        st.error(f"File `{path}` not found. Please upload or place it next to the script.")
        st.stop()

    try:
        df = pd.read_csv(path)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    df = df.dropna(subset=[DATE_COL])
    df["playtime_s"] = df["ms_played"] / 1000
    return df


# ---------- UI ----------
st.title("🎧 Spotify History Analysis")
st.markdown(
    "Upload or place your `spotify_history.csv` next to this script to get started."
)

df = load_data(CSV_PATH)

with st.sidebar:
    st.header("🔍 Filters")
    artists = st.multiselect(
        "Artists",
        options=sorted(df["artist_name"].unique()),
        default=sorted(df["artist_name"].unique()),
    )
    albums = st.multiselect(
        "Albums",
        options=sorted(df["album_name"].unique()),
        default=sorted(df["album_name"].unique()),
    )
    platforms = st.multiselect(
        "Platforms",
        options=sorted(df["platform"].unique()),
        default=sorted(df["platform"].unique()),
    )

# ---------- FILTER ----------
filtered = df[
    df["artist_name"].isin(artists)
    & df["album_name"].isin(albums)
    & df["platform"].isin(platforms)
]

if filtered.empty:
    st.warning("No data matches your current filters.")
    st.stop()

# ---------- METRICS ----------
total_ms = filtered["ms_played"].sum()
total_h = total_ms / 3_600_000
st.metric("Total Listening Time", f"{total_h:,.1f} h")

# ---------- TABLES ----------
st.subheader("Top 10 Artists")
top_artists = (
    filtered.groupby("artist_name")["ms_played"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    / 3_600_000
)
st.dataframe(top_artists.rename("Hours").reset_index(), use_container_width=True)

st.subheader("Top 10 Tracks")
top_tracks = (
    filtered.groupby("track_name")["ms_played"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    / 3_600_000
)
st.dataframe(top_tracks.rename("Hours").reset_index(), use_container_width=True)

# ---------- CHARTS ----------
st.subheader("Listening by Hour of Day")
hourly = (
        filtered[DATE_COL]
        .dt.hour
        .value_counts()
        .sort_index()
        .rename_axis("hour")
        .reset_index(name="plays")
    )
chart = (
        alt.Chart(hourly)
        .mark_line(color="red", point=True)
        .encode(
            x=alt.X("hour:O", title="Hour of Day"),
            y=alt.Y("plays:Q", title="Plays"),
            tooltip=["hour", "plays"],
        )
        .properties(height=300)
    )
st.altair_chart(chart, use_container_width=True)


st.subheader("Playtime Distribution")
play5 = filtered[filtered["playtime_s"] >= 5]
chart = (
        alt.Chart(play5)
        .mark_bar()
        .encode(
            x=alt.X("playtime_s", bin=alt.Bin(maxbins=50), title="Playtime (s)"),
            y="count()",
            color=alt.Color("playtime_s", scale=alt.Scale(scheme="set2"))
        )
        .properties(height=300)
    )
st.altair_chart(chart, use_container_width=True)

# Top Platforms
st.subheader("Top Platforms")
platform_counts = filtered["platform"].value_counts().reset_index()
platform_counts.columns = ["platform", "count"]

chart = (
    alt.Chart(platform_counts)
    .mark_bar()
    .encode(
        x=alt.X("count:Q"),
        y=alt.Y("platform:N", sort="-x"),
        color=alt.Color("platform:N", scale=alt.Scale(scheme="set2")),
    )
    .properties(height=300)
)
st.altair_chart(chart, use_container_width=True)

# ---------- RAW DATA ----------
with st.expander("Show filtered raw data"):
    st.dataframe(filtered, use_container_width=True)

