--Creating Views for Analytics
SELECT
    COUNT(*)                    AS total_invoices,
    COUNT(DISTINCT client_id)   AS total_clients,
    SUM(total)                  AS total_revenue,
    AVG(total)                  AS avg_invoice_value,
    MIN(invoice_date)           AS first_invoice_date,
    MAX(invoice_date)           AS last_invoice_date
FROM invoices;
----------------------------------------------------------------
CREATE OR REPLACE VIEW v_monthly_invoice_performance AS
SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    COUNT(*)                          AS invoice_count,
    SUM(total)                        AS revenue,
    AVG(total)                        AS avg_invoice_value
FROM invoices
GROUP BY 1
ORDER BY 1;
----------------------------------------------------------------

CREATE OR REPLACE VIEW v_client_revenue AS
SELECT
    client_id,
    COUNT(*)  AS invoice_count,
    SUM(total) AS total_revenue
FROM invoices
GROUP BY client_id
ORDER BY total_revenue DESC;
