#!/bin/bash

#python -m unittest discover || exit 1

gcloud functions deploy extract-summary-bert  \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_call \
    --runtime python37 \
    --trigger-http \
    --memory 256 \
    --vpc-connector tldr-cf-vpc-connector \
    --service-account summarizer@tldr-278619.iam.gserviceaccount.com || exit 1

sleep 5

python functional_test.py || exit 1
