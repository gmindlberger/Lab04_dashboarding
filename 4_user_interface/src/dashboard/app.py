# ================================================================
#  Gold-Layer Dashboard  – Weather • Retail • Retail × Weather
# ================================================================
#
#  TAB 1  🌤️ Weather            gold/weather/weather_aggregated.parquet
#  TAB 2  🛒 Retail             gold/retail/retail_aggregated.parquet
#  TAB 3  🔄 Retail × Weather   gold/retail_weather/retail_weather_combined.parquet
# ----------------------------------------------------------------

import os
from io import BytesIO

import boto3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_echarts import st_echarts

# ────────────────────────────────────────────────────────────────
# Page-Setup & helpers
# ────────────────────────────────────────────────────────────────
st.set_page_config("Gold-Layer Dashboard", "🌟", layout="wide")

def env(key: str, default: str) -> str:
    return os.getenv(key, default)

BUCKET      = env("BUCKET_NAME",        "batch-bucket")
WEATHER_KEY = env("GOLD_FILE_NAME",     "gold/weather/weather_aggregated.parquet")
RETAIL_KEY  = env("RETAIL_FILE_NAME",   "gold/retail/retail_aggregated.parquet")
COMBO_KEY   = env("COMBINED_FILE_NAME", "gold/retail_weather/retail_weather_combined.parquet")

s3 = boto3.client(
    "s3",
    endpoint_url=env("MINIO_ENDPOINT", "http://localhost:9000"),
    aws_access_key_id=env("MINIO_ACCESS_KEY", "admin"),
    aws_secret_access_key=env("MINIO_SECRET_KEY", "password"),
)

@st.cache_data(ttl="10m", show_spinner="📦 Lade Daten …")
def read_parquet(key: str) -> pd.DataFrame:
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return pd.read_parquet(BytesIO(obj["Body"].read()))

weather_df = read_parquet(WEATHER_KEY)
retail_df  = read_parquet(RETAIL_KEY)
combo_df   = read_parquet(COMBO_KEY)

# ----------------------------------------------------------------
tab_w, tab_r, tab_c = st.tabs(["🌤️ Weather", "🛒 Retail", "🔄 Retail × Weather"])

# ════════════════════════════════════════════════════════════════
# 1) WEATHER
# ════════════════════════════════════════════════════════════════
with tab_w:
    st.header("Weather – Gold Layer")

    # ─── Filter-Widgets ──────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)

    cats_all = sorted(weather_df["temperature_category"].dropna().unique())
    sel_cats = c1.multiselect("Temperature Category", cats_all, cats_all, key="w_cat")

    seasons_all = sorted(weather_df["season"].unique())
    sel_seas = c2.multiselect("Season", seasons_all, seasons_all, key="w_seas")

    def rng(df, col): return float(df[col].min()), float(df[col].max())

    t_min, t_max = rng(weather_df, "avg_temp")
    h_min, h_max = rng(weather_df, "avg_humidity")
    w_min, w_max = rng(weather_df, "avg_wind_speed")

    temp_rng = c3.slider("Temp °C",  t_min, t_max, (t_min, t_max), 0.1, key="w_tmp")
    hum_rng  = c4.slider("Hum %",   h_min, h_max, (h_min, h_max), 0.5, key="w_hum")
    wind_rng = c5.slider("Wind m/s", w_min, w_max, (w_min, w_max), 0.1, key="w_win")

    # ─── Datensatz filtern ──────────────────────────────────────
    wdf = weather_df.copy()
    if sel_cats: wdf = wdf[wdf["temperature_category"].isin(sel_cats)]
    if sel_seas: wdf = wdf[wdf["season"].isin(sel_seas)]
    wdf = wdf[
        wdf["avg_temp"].between(*temp_rng) &
        wdf["avg_humidity"].between(*hum_rng) &
        wdf["avg_wind_speed"].between(*wind_rng)
    ]

    # ─── KPIs ───────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Rows", f"{len(wdf):,}")
    k2.metric("Ø Temp (°C)", f"{wdf['avg_temp'].mean():.1f}")
    k3.metric("Ø Humidity (%)", f"{wdf['avg_humidity'].mean():.0f}")
    k4.metric("Ø Wind (m/s)", f"{wdf['avg_wind_speed'].mean():.1f}")

    # Distributions
    st.subheader("Distributions")
    sel_num = st.multiselect("Numeric Columns",
                             ["avg_temp","avg_humidity","avg_wind_speed"],
                             ["avg_temp"], key="w_num")
    for col in sel_num:
        fig, ax = plt.subplots(figsize=(5,2))
        sns.kdeplot(wdf[col], fill=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
        st.pyplot(fig)

    if not wdf.empty:
        # Count by Season
        st.subheader("Count by Season")
        cnt = wdf["season"].value_counts().reset_index(name="count").rename(columns={"index":"season"})
        fig_c, ax_c = plt.subplots(figsize=(5,2))
        sns.barplot(data=cnt, x="season", y="count", palette="viridis", ax=ax_c)
        st.pyplot(fig_c)

        # Radar Chart
        st.subheader("Seasonal Averages (Radar)")
        rd = (
            wdf.groupby("season")
               .agg(T=("avg_temp","mean"), H=("avg_humidity","mean"), W=("avg_wind_speed","mean"))
               .round(2).reset_index()
        )
        indicators = [
            {"name":"Temp (°C)","max":40},
            {"name":"Hum (%)","max":100},
            {"name":"Wind (m/s)","max":25}
        ]
        series = [{"value":[r.T, r.H, r.W], "name":r.season} for r in rd.itertuples()]
        opt = {"legend":{"data":rd["season"].tolist()},
               "radar":{"indicator":indicators,"radius":"60%"},
               "series":[{"type":"radar","data":series,"areaStyle":{"opacity":0.1}}]}
        st_echarts(opt, height="500px", key="w_radar")

    st.subheader("Weather Data")
    AgGrid(wdf, gridOptions=GridOptionsBuilder.from_dataframe(wdf).build(), height=300)

# ════════════════════════════════════════════════════════════════
# 2) RETAIL
# ════════════════════════════════════════════════════════════════
with tab_r:
    st.header("Retail – Gold Layer")

    stores_all  = sorted(retail_df["store_name"].unique())
    prods_all   = sorted(retail_df["product_name"].unique())
    seasons_all = sorted(retail_df["season"].unique())

    r1,r2,r3 = st.columns(3)
    sel_store = r1.multiselect("Store",  stores_all, stores_all, key="r_store")
    sel_prod  = r2.multiselect("Product",prods_all,  prods_all,  key="r_prod")
    sel_seas  = r3.multiselect("Season", seasons_all,seasons_all,key="r_sea")

    y_min, y_max = int(retail_df["year"].min()), int(retail_df["year"].max())
    yr_rng = st.slider("Year Range", y_min, y_max, (y_min, y_max), key="r_year")

    rdf = retail_df.copy()
    if sel_store: rdf = rdf[rdf["store_name"].isin(sel_store)]
    if sel_prod:  rdf = rdf[rdf["product_name"].isin(sel_prod)]
    if sel_seas:  rdf = rdf[rdf["season"].isin(sel_seas)]
    rdf = rdf[rdf["year"].between(*yr_rng)]

    k1, k2, k3 = st.columns(3)
    k1.metric("Rows", f"{len(rdf):,}")
    k2.metric("Σ Revenue (€)", f"{rdf['total_revenue'].sum():,.0f}")
    k3.metric("Ø Revenue (€)", f"{rdf['avg_revenue'].mean():,.2f}")

    st.subheader("Revenue by Store")
    if not rdf.empty:
        rev_store = rdf.groupby("store_name")["total_revenue"].sum().reset_index()
        fig_r, ax_r = plt.subplots(figsize=(5,2))
        sns.barplot(data=rev_store, x="store_name", y="total_revenue", palette="rocket", ax=ax_r)
        ax_r.set_ylabel("Revenue (€)")
        ax_r.set_xlabel("Store")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig_r)

    st.subheader("Retail Data")
    AgGrid(rdf, gridOptions=GridOptionsBuilder.from_dataframe(rdf).build(), height=300)

# ════════════════════════════════════════════════════════════════
# 3) RETAIL × WEATHER
# ════════════════════════════════════════════════════════════════
with tab_c:
    st.header("Retail × Weather – Combined Gold Layer")

    stores_all  = sorted(combo_df["store_name"].unique())
    prods_all   = sorted(combo_df["product_name"].unique())
    seasons_all = sorted(combo_df["season_x"].unique())

    c1,c2,c3 = st.columns(3)
    f_store = c1.multiselect("Store",   stores_all, stores_all, key="c_store")
    f_prod  = c2.multiselect("Product", prods_all,  prods_all,  key="c_prod")
    f_seas  = c3.multiselect("Season",  seasons_all,seasons_all,key="c_seas")

    cdf = combo_df.copy()
    if f_store: cdf = cdf[cdf["store_name"].isin(f_store)]
    if f_prod:  cdf = cdf[cdf["product_name"].isin(f_prod)]
    if f_seas:  cdf = cdf[cdf["season_x"].isin(f_seas)]

    k1,k2,k3 = st.columns(3)
    k1.metric("Rows", f"{len(cdf):,}")
    k2.metric("Σ Revenue (€)", f"{cdf['revenue'].sum():,.0f}")
    k3.metric("Ø Temp (°C)", f"{cdf['temperature'].mean():.1f}")

    st.subheader("Temperature vs Revenue")
    if not cdf.empty:
        fig_c, ax_c = plt.subplots(figsize=(5,2))
        sizes = cdf["quantity_sold"]/cdf["quantity_sold"].max()*300
        sns.scatterplot(
            data=cdf, x="temperature", y="revenue",
            hue="season_x",
            size=sizes, sizes=(20,300),
            ax=ax_c, legend=False
        )
        ax_c.set_xlabel("Temp (°C)")
        ax_c.set_ylabel("Revenue (€)")
        st.pyplot(fig_c)

    st.subheader("Combined Data")
    AgGrid(cdf, gridOptions=GridOptionsBuilder.from_dataframe(cdf).build(), height=300)

# ----------------------------------------------------------------
st.info("Data auto-refreshes on reload (cache TTL 10 min).")
