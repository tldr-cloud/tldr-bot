#!/bin/zsh

MODEL_NAME="bert_summaryzer"
ENDPOINT=https://alpha-ml.googleapis.com/v1
PROJECT_NAME="tldr-278619"

curl -X POST -v -k -H "Content-Type: application/json" -d "{'name': '"${MODEL_NAME}"'}" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    "${ENDPOINT}/projects/${PROJECT_NAME}/models/"