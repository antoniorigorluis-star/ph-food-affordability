-- Every region x month x basket item, with the price to use.
-- A few region/item pairs are never priced by PSA (e.g. eggs in Central Visayas).
-- For those we use the average price of the other regions that month and flag it,
-- so every region's basket has the same items and can be compared fairly.

DROP VIEW IF EXISTS basket_prices;
CREATE VIEW basket_prices AS
WITH regions AS (
    SELECT DISTINCT region_code, region_name, region_order FROM prices
),
months AS (
    SELECT DISTINCT month FROM prices
),
grid AS (                     -- one row for every region, month and basket item
    SELECT r.region_code, r.region_name, r.region_order, m.month,
           b.item_key, b.label, b.commodity, b.quantity, b.unit
    FROM regions r
    CROSS JOIN months m
    CROSS JOIN basket b
),
avg_all_regions AS (          -- fallback price: average across regions that month
    SELECT commodity, month, AVG(price) AS avg_price
    FROM prices
    WHERE commodity IN (SELECT commodity FROM basket)
    GROUP BY commodity, month
)
SELECT g.*,
       p.price                          AS region_price,
       COALESCE(p.price, a.avg_price)   AS price,
       CASE WHEN p.price IS NULL THEN 1 ELSE 0 END AS is_filled
FROM grid g
LEFT JOIN prices p
       ON p.region_code = g.region_code AND p.month = g.month AND p.commodity = g.commodity
LEFT JOIN avg_all_regions a
       ON a.commodity = g.commodity AND a.month = g.month;
