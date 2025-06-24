import os
from io import BytesIO

import boto3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

#UI Components from streamlit
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_echarts import st_echarts

# -----------------------------------------------------------------------------
# Streamlit-Page-Config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gold Layer Weather Dashboard",
    page_icon="🌟",
    layout="wide",
)

# -----------------------------------------------------------------------------
# Read Environment variables
# -----------------------------------------------------------------------------
def get_env_default(key: str, default_val: str) -> str:
    val = os.environ.get(key)
    return val if val else default_val

# MinIO-Konfiguration
MINIO_ENDPOINT   = get_env_default("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = get_env_default("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = get_env_default("MINIO_SECRET_KEY", "password")
BUCKET_NAME      = get_env_default("BUCKET_NAME", "weather-data")
GOLD_FILE_NAME   = get_env_default("GOLD_FILE_NAME", "gold/weather_aggregated.parquet")

# MinIO-Client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

# -----------------------------------------------------------------------------
# Data loading & caching
# -----------------------------------------------------------------------------
@st.cache_data(ttl="10m", show_spinner="📦 Lade Daten …")
def load_data() -> pd.DataFrame:
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=GOLD_FILE_NAME)
    df = pd.read_parquet(BytesIO(obj["Body"].read()))

    # get sure to serve numerical columns
    for col in ["avg_temp", "avg_humidity", "avg_wind_speed"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # parse date to pandas date format
    if "date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()

# -----------------------------------------------------------------------------
# Sidebar-filters
# -----------------------------------------------------------------------------
st.title("🌟 Gold Layer Weather Data Dashboard")
st.sidebar.header("Filters")

# --- Temperature Category (MULTI-SELECT) ------------------------------------
all_cats = sorted(df["temperature_category"].dropna().unique())
sel_cats = st.sidebar.multiselect(
    "Temperature Category",
    options=all_cats,
    default=all_cats,          # ⇒ standardmäßig alles gewählt
)

# --- Season ------------------------------------------------------------------
if "season" in df.columns:
    seasons = st.sidebar.multiselect(
        "Season",
        sorted(df["season"].unique()),
        default=list(df["season"].unique()),
    )
else:
    seasons = []

# --- Date Range --------------------------------------------------------------
if "date" in df.columns:
    dmin, dmax = df["date"].min().date(), df["date"].max().date()
    date_range = st.sidebar.date_input(
        "Date Range", (dmin, dmax), min_value=dmin, max_value=dmax
    )
else:
    date_range = None

# --- Numeric Slider Helper ---------------------------------------------------
def num_slider(col: str, label: str, step: float, fmt: str):
    if col not in df.columns:
        return None
    cmin, cmax = float(df[col].min()), float(df[col].max())
    return st.sidebar.slider(label, cmin, cmax, (cmin, cmax), step=step, format=fmt)

temp_range  = num_slider("avg_temp",       "Ø Temperature (°C)", 0.1, "%0.1f")
hum_range   = num_slider("avg_humidity",   "Ø Humidity (%)",     0.1, "%0.1f")
wind_range  = num_slider("avg_wind_speed", "Ø Wind Speed (m/s)", 0.1, "%0.1f")

# -----------------------------------------------------------------------------
# Finally filter our data
# -----------------------------------------------------------------------------
filtered_df = df.copy()

# Temp-Category: just filter, if some category is picked
if sel_cats:
    filtered_df = filtered_df[filtered_df["temperature_category"].isin(sel_cats)]

if seasons:
    filtered_df = filtered_df[filtered_df["season"].isin(seasons)]
if date_range and len(date_range) == 2:
    filtered_df = filtered_df.query("@date_range[0] <= date <= @date_range[1]")
if temp_range:
    filtered_df = filtered_df[filtered_df["avg_temp"].between(*temp_range)]
if hum_range:
    filtered_df = filtered_df[filtered_df["avg_humidity"].between(*hum_range)]
if wind_range:
    filtered_df = filtered_df[filtered_df["avg_wind_speed"].between(*wind_range)]

# -----------------------------------------------------------------------------
# KPI-Metrics
# -----------------------------------------------------------------------------
st.subheader("Key Metrics")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Rows", f"{len(filtered_df):,}")
if "avg_temp" in filtered_df.columns:
    c2.metric("Ø Temp (°C)", f"{filtered_df['avg_temp'].mean():.1f}")
if "avg_humidity" in filtered_df.columns:
    c3.metric("Ø Humidity (%)", f"{filtered_df['avg_humidity'].mean():.0f}")
if "avg_wind_speed" in filtered_df.columns:
    c4.metric("Ø Wind (m/s)", f"{filtered_df['avg_wind_speed'].mean():.1f}")

# -----------------------------------------------------------------------------
# Datatable via AG-Grid
# -----------------------------------------------------------------------------
st.subheader("Filtered Data")
gob = GridOptionsBuilder.from_dataframe(filtered_df)
gob.configure_pagination(paginationAutoPageSize=True)
AgGrid(filtered_df, gridOptions=gob.build(), height=400, fit_columns_on_grid_load=True)

# -----------------------------------------------------------------------------
# Distributions
# -----------------------------------------------------------------------------
st.subheader("Distributions")
num_cols = [c for c in ["avg_temp", "avg_humidity", "avg_wind_speed"] if c in filtered_df.columns]
chosen_cols = st.multiselect("Numeric Columns", num_cols, default=num_cols[:1])

for col in chosen_cols:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(filtered_df[col], fill=True, ax=ax)
    ax.set(title=f"Distribution of {col}", xlabel=col, ylabel="Frequency")
    st.pyplot(fig)

# -----------------------------------------------------------------------------
# Count by Season
# -----------------------------------------------------------------------------
if "season" in filtered_df.columns and not filtered_df.empty:
    st.subheader("Count by Season")
    season_cnt = (
        filtered_df["season"].value_counts()
        .reset_index(name="count")
        .rename(columns={"index": "season"})
    )
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=season_cnt, x="season", y="count", palette="viridis", ax=ax2)
    ax2.set_xlabel("Season")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

# -----------------------------------------------------------------------------
# Radar-Chart – Seasonal Averages (Temp / Humidity / Wind)
# -----------------------------------------------------------------------------
if "season" in filtered_df.columns and not filtered_df.empty:
    st.subheader("Seasonal Averages (Radar Chart)")

    radar_df = (
        filtered_df.groupby("season", as_index=False)
        .agg(
            avg_temp=("avg_temp", "mean"),
            avg_humidity=("avg_humidity", "mean"),
            avg_wind_speed=("avg_wind_speed", "mean"),
        )
        .round(2)
    )

    indicators = [
        {"name": "Temp (°C)",    "max": 40},
        {"name": "Humidity (%)", "max": 100},
        {"name": "Wind (m/s)",   "max": 25},
    ]

    series_data = [
        {
            "value": [row["avg_temp"], row["avg_humidity"], row["avg_wind_speed"]],
            "name": row["season"],
        }
        for _, row in radar_df.iterrows()
    ]

    option = {
        "legend": {"data": radar_df["season"].tolist()},
        "radar":  {"indicator": indicators, "radius": "70%"},
        "series": [{
            "type": "radar",
            "data": series_data,
            "areaStyle": {"opacity": 0.1},
        }],
    }
    st_echarts(option, height="700px", width="100%")

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.info("Data auto-refreshes on reload (cache TTL 10 min).")
