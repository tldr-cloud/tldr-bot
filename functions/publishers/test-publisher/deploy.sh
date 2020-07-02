#!/bin/bash

python3 -m pip install -r ./requirements.txt || exit 1

python3 main.py || exit 1

gcloud3 functions deploy test-publisher \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point function_call_publish \
    --runtime python37 \
    --memory 512 \
    --trigger-topic "processed-urls-test" \
    --service-account final-publisher@tldr-278619.iam.gserviceaccount.com || exit 1
