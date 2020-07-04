#!/bin/zsh

MODEL_NAME="bert_summaryzer"
ENDPOINT=https://alpha-ml.googleapis.com/v1
PROJECT_NAME="tldr-278619"
VERSION_NAME="v1"

curl -X GET -k -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "${ENDPOINT}/projects/${PROJECT_NAME}/models/${MODEL_NAME}/versions/${VERSION_NAME}"