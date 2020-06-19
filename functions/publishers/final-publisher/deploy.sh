#!/bin/bash

gcloud functions deploy final-publisher \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point function_call_publish \
    --runtime python37 \
    --memory 128 \
    --trigger-topic "prod-publish-events-topic" \
    --service-account final-publisher@tldr-278619.iam.gserviceaccount.com