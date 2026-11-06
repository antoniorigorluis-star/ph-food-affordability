-- Basket cost per region per month, joined to the minimum wage in force that month.
--
-- "In force" = the latest wage order whose effective date is on or before the 15th
-- of the month (PSA prices are monthly averages, so mid-month is the fairest match).
-- Regions with no rows in wages.csv get NULL wage and NULL hours: they still show
-- basket cost, and fill in automatically once their wage orders are added.
--
-- hours_needed = basket_cost / (daily_wage / 8)     (8-hour working day)
-- days_needed  = basket_cost / daily_wage

DROP VIEW IF EXISTS basket_monthly;
CREATE VIEW basket_monthly AS
WITH cost AS (
    SELECT region_code, region_name, region_order, month,
           ROUND(SUM(price * quantity), 2) AS basket_cost,
           SUM(is_filled)                  AS items_filled
    FROM basket_prices
    GROUP BY region_code, region_name, region_order, month
)
SELECT c.region_code, c.region_name, c.region_order, c.month,
       c.basket_cost, c.items_filled,
       w.wage_order,
       w.daily_wage,
       ROUND(c.basket_cost / (w.daily_wage / 8.0), 1) AS hours_needed,
       ROUND(c.basket_cost / w.daily_wage, 2)         AS days_needed
FROM cost c
LEFT JOIN wages w
       ON w.region_code = c.region_code
      AND w.effective_date = (
            SELECT MAX(w2.effective_date)
            FROM wages w2
            WHERE w2.region_code = c.region_code
              AND w2.effective_date <= date(c.month, '+14 days')
          );
