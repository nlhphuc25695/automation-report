#!/usr/bin/env bash
set -euo pipefail

# Required env vars:
# PROJECT_ID
# Optional:
# REGION, JOB_NAME, GAR_REPO, IMAGE_TAG, JOB_ARGS, SCHEDULER_NAME, SCHEDULER_CRON, TIMEZONE, SCHEDULER_SA

PROJECT_ID=${PROJECT_ID:?Missing PROJECT_ID}
REGION=${REGION:-asia-southeast1}
JOB_NAME=${JOB_NAME:-report-automation-monthly}
GAR_REPO=${GAR_REPO:-report-automation}
IMAGE_TAG=${IMAGE_TAG:-latest}
JOB_ARGS=${JOB_ARGS:-"run,--config,config/clients.yaml,--credentials,config/ads_credentials.yaml"}
SCHEDULER_NAME=${SCHEDULER_NAME:-report-automation-monthly}
SCHEDULER_CRON=${SCHEDULER_CRON:-"0 2 1 * *"}
TIMEZONE=${TIMEZONE:-"Asia/Ho_Chi_Minh"}
SCHEDULER_SA=${SCHEDULER_SA:-"scheduler@$PROJECT_ID.iam.gserviceaccount.com"}

IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$GAR_REPO/$JOB_NAME:$IMAGE_TAG"

# Build and push image.
gcloud builds submit --project "$PROJECT_ID" --tag "$IMAGE_URI" .

# Deploy Cloud Run Job.
gcloud run jobs deploy "$JOB_NAME" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --image "$IMAGE_URI" \
  --args "$JOB_ARGS" \
  --tasks 1 \
  --max-retries 1

# Create/update Cloud Scheduler HTTP trigger for Cloud Run Jobs API.
JOB_RUN_URI="https://run.googleapis.com/v2/projects/$PROJECT_ID/locations/$REGION/jobs/$JOB_NAME:run"

if gcloud scheduler jobs describe "$SCHEDULER_NAME" --location "$REGION" --project "$PROJECT_ID" >/dev/null 2>&1; then
  gcloud scheduler jobs update http "$SCHEDULER_NAME" \
    --project "$PROJECT_ID" \
    --location "$REGION" \
    --schedule "$SCHEDULER_CRON" \
    --time-zone "$TIMEZONE" \
    --http-method POST \
    --uri "$JOB_RUN_URI" \
    --oauth-service-account-email "$SCHEDULER_SA" \
    --headers "Content-Type=application/json" \
    --message-body "{}"
else
  gcloud scheduler jobs create http "$SCHEDULER_NAME" \
    --project "$PROJECT_ID" \
    --location "$REGION" \
    --schedule "$SCHEDULER_CRON" \
    --time-zone "$TIMEZONE" \
    --http-method POST \
    --uri "$JOB_RUN_URI" \
    --oauth-service-account-email "$SCHEDULER_SA" \
    --headers "Content-Type=application/json" \
    --message-body "{}"
fi

echo "Deployed Cloud Run Job and Scheduler trigger."
