#!/bin/bash

gcloud functions deploy add-url-pub \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_function_request \
    --runtime python37 \
    --trigger-http \
    --memory 512 \
    --service-account urls-processor@tldr-278619.iam.gserviceaccount.com