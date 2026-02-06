#!/usr/bin/env bash
set -euo pipefail

# Required env vars:
# PROJECT_ID, REGION
# Secrets to create (file paths):
# META_TOKEN_FILE, GOOGLE_ADS_TOKEN_FILE, TIKTOK_TOKEN_FILE, SERVICE_ACCOUNT_JSON

PROJECT_ID=${PROJECT_ID:?Missing PROJECT_ID}
REGION=${REGION:-asia-southeast1}

create_secret() {
  local name=$1
  local file=$2
  if [[ ! -f "$file" ]]; then
    echo "Secret file not found: $file" >&2
    exit 1
  fi
  gcloud secrets create "$name" --project "$PROJECT_ID" --replication-policy="automatic" || true
  gcloud secrets versions add "$name" --project "$PROJECT_ID" --data-file="$file"
}

create_secret "meta_ads_token" "$META_TOKEN_FILE"
create_secret "google_ads_token" "$GOOGLE_ADS_TOKEN_FILE"
create_secret "tiktok_ads_token" "$TIKTOK_TOKEN_FILE"
create_secret "google_service_account" "$SERVICE_ACCOUNT_JSON"

echo "Secrets created/updated."
