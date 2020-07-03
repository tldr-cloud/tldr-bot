#!/bin/bash

gcloud functions deploy review-list-provider \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_function_request \
    --runtime python38 \
    --trigger-http \
    --memory 128 \
    --service-account admin-site-api-agent@tldr-278619.iam.gserviceaccount.com  || exit 1
