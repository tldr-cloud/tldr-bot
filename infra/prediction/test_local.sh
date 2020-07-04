#!/bin/zsh

curl -X POST -k -H "Content-Type: application/json" \
    -d @request.json \
    "localhost:5000/summarize"

curl "localhost:5000/healthcheck"