#!/bin/sh
CONTAINER_NAME="kafka"
TOPIC_NAME="weather-data-pipeline"
KAFKA_HOST="kafka:9092"

docker exec -it ${CONTAINER_NAME} \
  kafka-topics.sh --create \
  --bootstrap-server ${KAFKA_HOST} \
  --topic ${TOPIC_NAME} \
  --partitions 1 \
  --replication-factor 1