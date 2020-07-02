#!/bin/bash

python -m unittest discover || exit 1

gcloud functions deploy new-url-processor  \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_function_all \
    --runtime python37 \
    --memory 512 \
    --trigger-topic "new-urls" \
    --service-account urls-processor@tldr-278619.iam.gserviceaccount.com