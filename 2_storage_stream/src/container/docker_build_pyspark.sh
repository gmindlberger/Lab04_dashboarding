#!/bin/sh

# use https://github.com/jupyter/docker-stacks.git and build a custom
# container image with a given spark version. 

SPARK_VERSION=3.5.5
HADOOP_VERSION=3
OPENJDK_VERSION=17
BASE_IMAGE_NAME=jupyter_pyspark
IMAGE_NAME="${BASE_IMAGE_NAME}:${SPARK_VERSION}"

docker build --rm --force-rm \
    -t ${IMAGE_NAME} ./docker-stacks/images/pyspark-notebook \
    --label "org.opencontainers.image.source=https://github.com/bihe/architecture-lab" \
    --build-arg openjdk_version=${OPENJDK_VERSION} \
    --build-arg spark_version=${SPARK_VERSION} \
    --build-arg hadoop_version=${HADOOP_VERSION} \
    --build-arg spark_download_url="https://archive.apache.org/dist/spark/"

docker run -it --rm ${IMAGE_NAME} pyspark --version

