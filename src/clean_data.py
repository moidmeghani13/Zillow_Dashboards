import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_FILE = DATA_DIR / "Zip_zhvi_uc_sfr_tier_0.33_0.67_sm_sa_month.csv"
OUTPUT_FILE = DATA_DIR / "processed" / "zhvi_long.parquet"

print("Loading raw Zillow data...")
df = pd.read_csv(RAW_FILE)

df = df.rename(columns={"RegionName": "zip"})
df["zip"] = df["zip"].astype(str).str.zfill(5)


id_cols = [
    "RegionID",
    "zip",
    "City",
    "State",
    "Metro",
    "CountyName",
    "SizeRank",
    "RegionType",
    "StateName"
]

print("Reshaping data to long format...")


long_df = df.melt(
    id_vars=id_cols,
    var_name="date",
    value_name="zhvi"
)

long_df["date"] = pd.to_datetime(long_df["date"])
long_df = long_df.dropna(subset=["zhvi"])

print("Calculating year-over-year growth...")
long_df = long_df.sort_values(["zip", "date"])

long_df["zhvi_yoy"] = (
    long_df
    .groupby("zip")["zhvi"]
    .pct_change(12)
)


OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
long_df.to_parquet(OUTPUT_FILE, index=False)
print("Done!")
print(f"Saved to: {OUTPUT_FILE}")

