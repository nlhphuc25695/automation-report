CREATE TABLE IF NOT EXISTS `{{project_id}}.{{dataset}}.ads_monthly_summary` (
  month DATE,
  platform STRING,
  client_id STRING,
  spend FLOAT64,
  impressions INT64,
  clicks INT64,
  ctr FLOAT64,
  cpc FLOAT64,
  conversions FLOAT64,
  cpa FLOAT64,
  roas FLOAT64
);
