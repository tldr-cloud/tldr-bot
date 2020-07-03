#!/bin/bash

gcloud functions deploy twitter-publisher \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_function_all \
    --runtime python38 \
    --memory 128 \
    --trigger-topic "twitter-publish-queue" \
    --service-account final-publisher@tldr-278619.iam.gserviceaccount.com || exit 1
