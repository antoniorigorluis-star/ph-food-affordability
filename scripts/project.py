from pathlib import Path
import pandas as pd

script_folder = Path(__file__).parent
raw_folder = script_folder / ".." / "data" / "raw"
tables = []

for file in sorted(raw_folder.glob("*.csv")):
    df = pd.read_csv(file, skiprows=1)
    # the category name only appears in each file's title line, so it would be lost when the files are stacked.
    df["source_file"] = file.stem
    tables.append(df)

prices_wide = pd.concat(tables, ignore_index=True)
prices_long = prices_wide.melt(
    id_vars=["Geolocation", "Commodity", "source_file"], 
    var_name="period", 
    value_name="price"
)

prices_monthly = prices_long[~prices_long["period"].str.contains("Annual")].copy()
prices_monthly["price"] = pd.to_numeric(prices_monthly["price"], errors="coerce")

prices_regions = prices_monthly[(prices_monthly["Geolocation"].str.startswith("..")) & (~prices_monthly["Geolocation"].str.startswith("...."))].copy()
prices_regions["region"] = prices_regions["Geolocation"].str.lstrip(".").str.split(" - ").str[0]

print(prices_regions["region"].value_counts())