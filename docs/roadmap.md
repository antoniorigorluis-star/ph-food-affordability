# Project Roadmap

**Question:** How many hours of minimum-wage work does it take to buy a basic food basket in each Philippine region, and how has that changed since 2020?

**Core calculation (per region, per month):**

```
hours_needed = basket_cost / (daily_minimum_wage / 8)
```

Example: basket ₱900, wage ₱500/day (₱62.50/hour) → 14.4 hours of work.

## Target tables

**prices** — one row per region, commodity and month

| region | commodity | month | price |
|---|---|---|---|
| NCR | RICE, REGULAR-MILLED, 1 KG | 2020-01 | 42.50 |

**wages** — one row per region per wage order

| region | effective_date | daily_wage |
|---|---|---|
| NCR | 2023-07-16 | 610 |

## Stages

- [x] **1. Get price data**: PSA OpenStat retail prices, 11 category files in `data/raw/`
- [x] **2. Combine the 11 files into one table**: so every later step runs once; basket items come from different files. Add `source_file` to keep each row's category. Check: shape `(23443, 120)`.
- [x] **3. Reshape wide → long**: turn 117 month columns into one `month` column, so the data can be filtered by date, joined to wages and queried in SQL.
- [x] **4. Fix values**: turn `".."` and `"."` into real missing values, and price text into numbers.
- [x] **5. Keep only the 18 regions**: (the usual 17 plus Negros Island Region, NIR, re-created in 2024) drop PHILIPPINES and province/city rows (wages are set per region), and standardize region names so they match the wage table. → `scripts/clean_prices.py`
- [x] **6. Choose the basket**: 12 items, weekly quantities for a family of five, with reasons → `data/manual/basket.csv`
- [ ] **7. Build the wage table**: pull region, effective date and daily wage from the NWPC wage orders → `data/manual/wages.csv` (NCR done; 17 regions to go; NCR-21 to NCR-25 still need checking against the PDFs)
- [x] **8. Load into SQLite and analyze**: `scripts/build_database.py` loads `data/ph_food.db` and runs `sql/01`–`04`
- [ ] **9. Dashboard and findings**: dashboard built (NCR hours, all-region basket cost); fill in Key Findings once all regions' wages are in.

## Re-running after you add wages

1. Add rows to `data/manual/wages.csv` (one per wage order, back to 2018 for the full trend).
2. `python scripts/build_database.py` (only re-run `clean_prices.py` when the PSA files change).
3. Replace the CSVs in the dashboard (Sources → replace file): `basket_monthly.csv`, `region_summary.csv`, `basket_items.csv`, `wages.csv`.

Cleaning decisions are recorded in [cleaning_log.md](cleaning_log.md).
