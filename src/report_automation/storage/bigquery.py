from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from typing import Iterable, List

from google.cloud import bigquery

from report_automation.models import AdsDailyRow, MonthlySummaryRow


@dataclass
class BigQueryConfig:
    project_id: str
    dataset: str


class BigQueryStore:
    def __init__(self, config: BigQueryConfig) -> None:
        self.config = config
        self._client = None

    @property
    def enabled(self) -> bool:
        if os.getenv("DRY_RUN") == "1":
            return False
        return bool(self.config.project_id and self.config.dataset)

    @property
    def client(self) -> bigquery.Client:
        if self._client is None:
            self._client = bigquery.Client(project=self.config.project_id)
        return self._client

    def ensure_dataset_and_tables(self) -> None:
        if not self.enabled:
            return

        dataset_ref = bigquery.DatasetReference(self.config.project_id, self.config.dataset)
        try:
            self.client.get_dataset(dataset_ref)
        except Exception:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            self.client.create_dataset(dataset, exists_ok=True)

        self._ensure_table("ads_daily_fact", _daily_schema())
        self._ensure_table("ads_monthly_summary", _monthly_schema())

    def _ensure_table(self, table_name: str, schema: List[bigquery.SchemaField]) -> None:
        table_ref = f"{self.config.project_id}.{self.config.dataset}.{table_name}"
        try:
            self.client.get_table(table_ref)
        except Exception:
            table = bigquery.Table(table_ref, schema=schema)
            self.client.create_table(table, exists_ok=True)

    def load_daily_rows(self, rows: Iterable[AdsDailyRow]) -> None:
        if not self.enabled:
            return
        rows_json = [
            {
                "date": row.date.isoformat(),
                "platform": row.platform,
                "account_id": row.account_id,
                "campaign_id": row.campaign_id,
                "adset_id": row.adset_id,
                "ad_id": row.ad_id,
                "spend": row.spend,
                "impressions": row.impressions,
                "clicks": row.clicks,
                "conversions": row.conversions,
                "revenue": row.revenue,
                "client_id": row.client_id,
                "currency": row.currency,
            }
            for row in rows
        ]
        if not rows_json:
            return
        table_ref = f"{self.config.project_id}.{self.config.dataset}.ads_daily_fact"
        job = self.client.load_table_from_json(rows_json, table_ref)
        job.result()

    def load_monthly_summary(self, rows: Iterable[MonthlySummaryRow]) -> None:
        if not self.enabled:
            return
        rows_json = [
            {
                "month": row.month.isoformat(),
                "platform": row.platform,
                "client_id": row.client_id,
                "spend": row.spend,
                "impressions": row.impressions,
                "clicks": row.clicks,
                "ctr": row.ctr,
                "cpc": row.cpc,
                "conversions": row.conversions,
                "cpa": row.cpa,
                "roas": row.roas,
            }
            for row in rows
        ]
        if not rows_json:
            return
        table_ref = f"{self.config.project_id}.{self.config.dataset}.ads_monthly_summary"
        job = self.client.load_table_from_json(rows_json, table_ref)
        job.result()

    def reset_client_month(self, client_id: str, month_start: date, month_end: date) -> None:
        if not self.enabled:
            return

        daily_query = f"""
        DELETE FROM `{self.config.project_id}.{self.config.dataset}.ads_daily_fact`
        WHERE client_id = @client_id
          AND date >= @month_start
          AND date < @month_end
        """
        monthly_query = f"""
        DELETE FROM `{self.config.project_id}.{self.config.dataset}.ads_monthly_summary`
        WHERE client_id = @client_id
          AND month = @month_start
        """
        params = [
            bigquery.ScalarQueryParameter("client_id", "STRING", client_id),
            bigquery.ScalarQueryParameter("month_start", "DATE", month_start),
            bigquery.ScalarQueryParameter("month_end", "DATE", month_end),
        ]
        config = bigquery.QueryJobConfig(query_parameters=params)
        self.client.query(daily_query, job_config=config).result()
        self.client.query(monthly_query, job_config=config).result()


def _daily_schema() -> List[bigquery.SchemaField]:
    return [
        bigquery.SchemaField("date", "DATE"),
        bigquery.SchemaField("platform", "STRING"),
        bigquery.SchemaField("account_id", "STRING"),
        bigquery.SchemaField("campaign_id", "STRING"),
        bigquery.SchemaField("adset_id", "STRING"),
        bigquery.SchemaField("ad_id", "STRING"),
        bigquery.SchemaField("spend", "FLOAT"),
        bigquery.SchemaField("impressions", "INTEGER"),
        bigquery.SchemaField("clicks", "INTEGER"),
        bigquery.SchemaField("conversions", "FLOAT"),
        bigquery.SchemaField("revenue", "FLOAT"),
        bigquery.SchemaField("client_id", "STRING"),
        bigquery.SchemaField("currency", "STRING"),
    ]


def _monthly_schema() -> List[bigquery.SchemaField]:
    return [
        bigquery.SchemaField("month", "DATE"),
        bigquery.SchemaField("platform", "STRING"),
        bigquery.SchemaField("client_id", "STRING"),
        bigquery.SchemaField("spend", "FLOAT"),
        bigquery.SchemaField("impressions", "INTEGER"),
        bigquery.SchemaField("clicks", "INTEGER"),
        bigquery.SchemaField("ctr", "FLOAT"),
        bigquery.SchemaField("cpc", "FLOAT"),
        bigquery.SchemaField("conversions", "FLOAT"),
        bigquery.SchemaField("cpa", "FLOAT"),
        bigquery.SchemaField("roas", "FLOAT"),
    ]
