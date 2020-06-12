#!/bin/bash

gcloud functions deploy summary-translator  \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_function_all \
    --runtime python37 \
    --memory 512 \
    --trigger-topic "processed-urls" \
    --service-account urls-processor@tldr-278619.iam.gserviceaccount.com