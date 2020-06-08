#!/bin/bash

gcloud functions deploy extract-summary  \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_call \
    --runtime python37 \
    --trigger-http \
    --memory 512 \
    --service-account summarizer@tldr-278619.iam.gserviceaccount.com