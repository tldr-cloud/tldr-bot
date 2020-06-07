#!/bin/bash

gcloud functions deploy final-publisher \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point function_call_publish \
    --runtime python37 \
    --memory 512 \
    --trigger-topic "processed-urls" \
    --service-account final-publisher@tldr-278619.iam.gserviceaccount.com