#!/bin/zsh

MODEL_NAME="bert_summaryzer"
VERSION_NAME="v3"
ENDPOINT=https://alpha-ml.googleapis.com/v1
PROJECT_NAME="tldr-278619"

curl -X POST -k -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "${ENDPOINT}/projects/${PROJECT_NAME}/models/${MODEL_NAME}/versions/${VERSION_NAME}:predict" \
    -d @request.json