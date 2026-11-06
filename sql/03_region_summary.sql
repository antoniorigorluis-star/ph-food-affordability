-- One row per region for the latest month of prices:
-- basket cost, change since January 2020, hours of work needed, and ranks.
-- Also shows hours at the region's NEWEST wage order, which can start after the
-- last month of prices (e.g. NCR-28 took effect 26 Sep 2026).

DROP VIEW IF EXISTS region_summary;
CREATE VIEW region_summary AS
WITH latest AS (
    SELECT MAX(month) AS month FROM basket_monthly
),
base AS (
    SELECT region_code, basket_cost AS cost_2020, hours_needed AS hours_2020
    FROM basket_monthly
    WHERE month = '2020-01-01'
),
newest_wage AS (              -- most recent wage order per region (window function)
    SELECT region_code, wage_order, effective_date, daily_wage
    FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY region_code ORDER BY effective_date DESC) AS rn
        FROM wages
    )
    WHERE rn = 1
),
joined AS (
    SELECT bm.*, b.cost_2020, b.hours_2020,
           nw.wage_order     AS newest_wage_order,
           nw.effective_date AS newest_wage_date,
           nw.daily_wage     AS newest_daily_wage
    FROM basket_monthly bm
    JOIN latest l ON bm.month = l.month
    LEFT JOIN base b ON b.region_code = bm.region_code
    LEFT JOIN newest_wage nw ON nw.region_code = bm.region_code
)
SELECT region_code, region_name, region_order, month,
       basket_cost,
       cost_2020,
       ROUND(100.0 * (basket_cost - cost_2020) / cost_2020, 1) AS cost_change_pct,
       wage_order, daily_wage,
       hours_needed, days_needed,
       hours_2020,
       ROUND(hours_needed - hours_2020, 1) AS hours_change,
       newest_wage_order, newest_wage_date, newest_daily_wage,
       ROUND(basket_cost / (newest_daily_wage / 8.0), 1) AS hours_at_newest_wage,
       RANK() OVER (ORDER BY basket_cost DESC) AS cost_rank,
       CASE WHEN hours_needed IS NOT NULL
            THEN RANK() OVER (PARTITION BY hours_needed IS NULL ORDER BY hours_needed DESC)
       END AS hours_rank,
       items_filled
FROM joined;
