#!/bin/bash

docker run \
  -v $(pwd)/../../..:/home/ \
  -w /home/functions/publishers/final-publisher \
  gcr.io/tldr-278619/ci-agent \
  python3 -m pip install -r ./requirements.txt && \
  python3 -m unittest discover && \
  python3 main.py