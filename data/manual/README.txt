Hand-entered input tables. Edit these in Excel/Sheets, save as CSV, then re-run the scripts.

wages.csv   One row per region per wage order. Typed in from the NWPC wage order PDFs.
            region_code must be one of: NCR, CAR, I, II, III, IV-A, MIMAROPA, V, VI, NIR,
            VII, VIII, IX, X, XI, XII, XIII, BARMM
            daily_wage = the non-agriculture daily minimum wage in pesos.
            effective_date = YYYY-MM-DD (the "Date of Effectivity" at the end of the order).
            verified = confirmed / amount confirmed / not yet checked

basket.csv  The food basket: which PSA commodities, and how much of each per WEEK for a
            family of five. "commodity" must match the PSA name exactly.
