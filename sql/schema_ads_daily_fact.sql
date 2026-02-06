CREATE TABLE IF NOT EXISTS `{{project_id}}.{{dataset}}.ads_daily_fact` (
  date DATE,
  platform STRING,
  account_id STRING,
  campaign_id STRING,
  adset_id STRING,
  ad_id STRING,
  spend FLOAT64,
  impressions INT64,
  clicks INT64,
  conversions FLOAT64,
  revenue FLOAT64,
  client_id STRING,
  currency STRING
);
