-- Cost of each basket item per region, for January 2020 and the latest month,
-- to show which foods drive the basket and which got more expensive.

DROP VIEW IF EXISTS basket_items;
CREATE VIEW basket_items AS
SELECT bp.region_code, bp.region_name, bp.region_order,
       CASE WHEN bp.month = '2020-01-01' THEN 'jan_2020' ELSE 'latest' END AS period,
       bp.month, bp.item_key, bp.label, bp.quantity, bp.unit,
       ROUND(bp.price, 2)               AS price,
       ROUND(bp.price * bp.quantity, 2) AS item_cost,
       bp.is_filled
FROM basket_prices bp
WHERE bp.month = '2020-01-01'
   OR bp.month = (SELECT MAX(month) FROM prices);
