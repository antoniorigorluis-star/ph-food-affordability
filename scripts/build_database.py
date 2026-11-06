"""Step 7-8: load prices, wages and the basket into SQLite, run the SQL, export results.

Inputs:  data/processed/prices_regions.csv   (from clean_prices.py)
         data/manual/wages.csv               (typed in from NWPC wage orders)
         data/manual/basket.csv              (the food basket)
Output:  data/ph_food.db                     (open it in DB Browser for SQLite to explore)
         data/processed/basket_monthly.csv   (every region x month: basket cost, wage, hours)
         data/processed/region_summary.csv   (latest month per region, change since 2020)
         data/processed/basket_items.csv     (each item's cost, latest month vs Jan 2020)

Run:  python scripts/build_database.py
"""
from pathlib import Path
import sqlite3
import pandas as pd

project = Path(__file__).resolve().parent.parent
processed = project / "data" / "processed"
manual = project / "data" / "manual"
sql_folder = project / "sql"
db_file = project / "data" / "ph_food.db"

prices = pd.read_csv(processed / "prices_regions.csv")
wages = pd.read_csv(manual / "wages.csv")
basket = pd.read_csv(manual / "basket.csv")

# Checks: catch typos in the hand-entered files before they silently break the join
bad_regions = set(wages["region_code"]) - set(prices["region_code"])
assert not bad_regions, f"wages.csv has unknown region_code(s): {bad_regions}"
bad_items = set(basket["commodity"]) - set(prices["commodity"])
assert not bad_items, f"basket.csv has commodity names not found in the PSA data: {bad_items}"
pd.to_datetime(wages["effective_date"], format="%Y-%m-%d")  # fails loudly on a bad date

with sqlite3.connect(db_file) as con:
    prices.to_sql("prices", con, if_exists="replace", index=False)
    wages.to_sql("wages", con, if_exists="replace", index=False)
    basket.to_sql("basket", con, if_exists="replace", index=False)

    # The numbered .sql files create the views, in order
    for sql_file in sorted(sql_folder.glob("0*.sql")):
        con.executescript(sql_file.read_text(encoding="utf-8"))
        print(f"ran {sql_file.name}")

    exports = {
        "basket_monthly.csv": "SELECT * FROM basket_monthly ORDER BY region_order, month",
        "region_summary.csv": "SELECT * FROM region_summary ORDER BY region_order",
        "basket_items.csv": "SELECT * FROM basket_items ORDER BY region_order, period, item_key",
    }
    for name, query in exports.items():
        df = pd.read_sql(query, con)
        df.to_csv(processed / name, index=False)
        print(f"saved {name}: {len(df):,} rows")

    summary = pd.read_sql("SELECT region_code, month, basket_cost, daily_wage, hours_needed "
                          "FROM region_summary ORDER BY region_order", con)
    print(summary.to_string(index=False))
