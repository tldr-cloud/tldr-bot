#!/bin/bash

python3 -m pip install -r ./requirements.txt || exit 1

gcloud functions deploy tldr-voice-bot  \
    --region us-central1 \
    --project tldr-278619 \
    --entry-point process_call \
    --runtime python38 \
    --trigger-http \
    --memory 128 \
    --service-account tldr-voice-bot@tldr-278619.iam.gserviceaccount.com || exit 1
