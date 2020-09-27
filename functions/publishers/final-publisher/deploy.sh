#!/bin/bash

python3 -m pip install -r ./requirements.txt || exit 1

python3 -m unittest discover || exit 1

python3 main.py || exit 1

gcloud functions deploy final-publisher \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point function_call_publish \
    --runtime python37 \
    --memory 256 \
    --trigger-topic "prod-publish-events-topic" \
    --service-account final-publisher@tldr-278619.iam.gserviceaccount.com