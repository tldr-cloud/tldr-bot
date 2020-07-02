#!/bin/zsh

TAG="gcr.io/tldr-278619/ci-agent"

docker build --memory 8Gb -t "${TAG}" -f Dockerfile ./
docker push "${TAG}"
