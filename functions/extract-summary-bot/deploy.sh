#!/bin/bash

python -m unittest discover || exit 1

gcloud functions deploy extract-summary-bot  \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_call \
    --runtime python37 \
    --trigger-http \
    --memory 128 \
    --service-account summarizer@tldr-278619.iam.gserviceaccount.com || exit 1

python functional_test.py || exit 1
