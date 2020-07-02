#!/bin/bash

python -m pip install -r ./requirements.txt || exit 1

python -m unittest discover || exit 1

gcloud functions deploy add-url-pub \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_function_request \
    --runtime python37 \
    --trigger-http \
    --memory 512 \
    --service-account urls-processor@tldr-278619.iam.gserviceaccount.com || exit 1

sleep 5

python functional_test.py || exit 1