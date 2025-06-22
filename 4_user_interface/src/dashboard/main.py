import os
from io import BytesIO

import boto3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


# get the given key from the environment or use default value
def get_env_default(key: str, default_val: str) -> str:
    val = os.environ.get(key)
    if val is None or val == "":
        return default_val
    return val


# MinIO Configuration
MINIO_ENDPOINT = get_env_default("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = get_env_default("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = get_env_default("MINIO_SECRET_KEY", "password")
BUCKET_NAME = get_env_default("BUCKET_NAME", "weather-data")
GOLD_FILE_NAME = get_env_default("GOLD_FILE_NAME", "gold/weather_aggregated.parquet")

# Initialize MinIO Client
s3 = boto3.client(
    "s3", endpoint_url=MINIO_ENDPOINT, aws_access_key_id=MINIO_ACCESS_KEY, aws_secret_access_key=MINIO_SECRET_KEY
)


# Load Data from MinIO
@st.cache_data
def load_data():
    gold_obj = s3.get_object(Bucket=BUCKET_NAME, Key=GOLD_FILE_NAME)
    df = pd.read_parquet(BytesIO(gold_obj["Body"].read()))
    return df


df = load_data()

# Streamlit App UI
st.title("🌟 Gold Layer Weather Data Dashboard")
st.sidebar.header("Filters")

# --------------------------------------------------------------------------
# [TODO] additional filters
# --------------------------------------------------------------------------

# Filter Data
selected_category = st.sidebar.selectbox("Select Temperature Category", df["temperature_category"].unique())
filtered_df = df[df["temperature_category"] == selected_category]

# Display Data Summary
st.subheader("📊 Aggregated Data Overview")
st.write(filtered_df)

# Count by Temperature Category
st.subheader("📊 Count by Temperature Category")
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=df, x="temperature_category", y="count", palette="coolwarm", ax=ax, hue="temperature_category")
st.pyplot(fig)

# --------------------------------------------------------------------------
# [TODO] additional categories and plots
# --------------------------------------------------------------------------

st.write("🔄 Data auto-refreshes when reloaded.")
