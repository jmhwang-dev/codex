#!/bin/bash

set -e

USER=${1:-example}
IMAGE=ghcr.io/$USER/spark:4.0.0

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t "$IMAGE" . \
  --push
