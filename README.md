# Can Filipinos Afford Food? Regional Food Prices vs Wages

## Business Question
Is food affordable relative to regional wages in the Philippines, and how has that changed over time?

Specifically: how many hours of minimum-wage work does it take to buy a basic food basket in each Philippine region, and how has that changed since 2020?

## Data
- Food prices: PSA OpenStat (retail prices by region)
- Wages: DOLE NWPC regional minimum wage orders

## Tools
SQLite, Python (Pandas), D3.js dashboard on GitHub Pages

## Method
1. Cleaned and standardized region names, dates and units
2. Loaded data into SQLite
3. Analyzed with SQL (joins, window functions, ranking)
4. Built an interactive dashboard (`index.html`) that reads the exported CSVs, hosted on GitHub Pages

## Key Findings
1. (fill in after analysis)
2. (fill in after analysis)
3. (fill in after analysis)

## Dashboard
Live: https://YOUR-USERNAME.github.io/ph-food-affordability/

To view locally: run `python -m http.server` in this folder and open http://localhost:8000

## Limitations
- (e.g. gaps in price data for some regions or months)
- (e.g. minimum wage is not the same as actual earnings)

## Project Structure
```
data/raw/        original downloaded files (never edited)
data/processed/  cleaned CSVs produced by scripts
scripts/         Python cleaning scripts
sql/             analysis queries
notebooks/       exploration notebooks
docs/            cleaning_log.md and other notes
README.md
```
