"""Step 1-5: turn the 11 raw PSA price files into one clean, region-level table.

Output: data/processed/prices_regions.csv
        one row per region, commodity and month (only months that have a price)

Run from anywhere:  python scripts/clean_prices.py
"""
from pathlib import Path
import pandas as pd

project = Path(__file__).resolve().parent.parent
raw_folder = project / "data" / "raw"
out_file = project / "data" / "processed" / "prices_regions.csv"

# PSA's region label -> (short code used everywhere else, readable name).
# The code is what wages.csv uses, so prices and wages can be joined.
# Dictionary order = official region order, used to sort tables and charts.
REGIONS = {
    "NCR - National Capital Region": ("NCR", "NCR"),
    "CAR - Cordillera Administrative Region": ("CAR", "Cordillera (CAR)"),
    "I - Ilocos Region": ("I", "Ilocos"),
    "II - Cagayan Valley": ("II", "Cagayan Valley"),
    "III - Central Luzon": ("III", "Central Luzon"),
    "IV-A - CALABARZON": ("IV-A", "CALABARZON"),
    "MIMAROPA Region": ("MIMAROPA", "MIMAROPA"),
    "V - Bicol Region": ("V", "Bicol"),
    "VI - Western Visayas": ("VI", "Western Visayas"),
    "Negros Island Region (NIR)": ("NIR", "Negros Island"),
    "VII - Central Visayas": ("VII", "Central Visayas"),
    "VIII - Eastern Visayas": ("VIII", "Eastern Visayas"),
    "IX - Zamboanga Peninsula": ("IX", "Zamboanga Peninsula"),
    "X - Northern Mindanao": ("X", "Northern Mindanao"),
    "XI - Davao Region": ("XI", "Davao"),
    "XII - SOCCSKSARGEN": ("XII", "SOCCSKSARGEN"),
    "XIII - Caraga": ("XIII", "Caraga"),
    "BARMM - Bangsamoro Autonomous Region in Muslim Mindanao": ("BARMM", "BARMM"),
}

# Step 1 - combine the 11 category files (skip each file's title line, keep the category)
tables = []
for file in sorted(raw_folder.glob("*.csv")):
    df = pd.read_csv(file, skiprows=1)
    df["category"] = file.stem
    tables.append(df)
prices_wide = pd.concat(tables, ignore_index=True)

# Step 2 - wide to long: month columns become one "period" column
prices_long = prices_wide.melt(
    id_vars=["Geolocation", "Commodity", "category"], var_name="period", value_name="price"
)

# Step 3 - drop PSA's "Annual" averages (they are not months)
prices_long = prices_long[~prices_long["period"].str.contains("Annual")].copy()

# Step 4 - prices to numbers (".." and "." become NaN), period text to a real date
prices_long["price"] = pd.to_numeric(prices_long["price"], errors="coerce")
prices_long["month"] = pd.to_datetime(prices_long["period"], format="%Y %B")

# Step 5 - keep only the 18 regions and standardize their names
is_region = prices_long["Geolocation"].str.startswith("..") & ~prices_long["Geolocation"].str.startswith("....")
prices = prices_long[is_region].copy()
prices["psa_region"] = prices["Geolocation"].str.lstrip(".")

unknown = set(prices["psa_region"]) - set(REGIONS)
assert not unknown, f"New region label(s) in the PSA files, add them to REGIONS: {unknown}"

order = {label: i + 1 for i, label in enumerate(REGIONS)}
prices["region_code"] = prices["psa_region"].map(lambda r: REGIONS[r][0])
prices["region_name"] = prices["psa_region"].map(lambda r: REGIONS[r][1])
prices["region_order"] = prices["psa_region"].map(order)

# Keep only rows that have a price (missing months add nothing to the analysis)
prices = prices.dropna(subset=["price"])
prices = prices.rename(columns={"Commodity": "commodity"})
prices["month"] = prices["month"].dt.strftime("%Y-%m-%d")
prices = prices[["region_code", "region_name", "region_order", "category", "commodity", "month", "price"]]
prices = prices.sort_values(["region_order", "category", "commodity", "month"])

out_file.parent.mkdir(parents=True, exist_ok=True)
prices.to_csv(out_file, index=False)

print(f"Saved {len(prices):,} rows to {out_file.relative_to(project)}")
print(f"Regions: {prices['region_code'].nunique()}  Commodities: {prices['commodity'].nunique()}  "
      f"Months: {prices['month'].min()} to {prices['month'].max()}")
