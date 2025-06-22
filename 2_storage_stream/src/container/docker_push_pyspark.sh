#!/bin/sh

# use https://github.com/jupyter/docker-stacks.git and build a custom
# container image with a given spark version. 

BASE_IMAGE_NAME=jupyter_pyspark
IMAGE_NAME="${BASE_IMAGE_NAME}:${SPARK_VERSION}"

docker tag ${IMAGE_NAME} "ghcr.io/bihe/architecture-lab/${BASE_IMAGE_NAME}:latest" 
docker tag ${IMAGE_NAME} "ghcr.io/bihe/architecture-lab/${IMAGE_NAME}" 
docker push -a "ghcr.io/bihe/architecture-lab/${BASE_IMAGE_NAME}"
