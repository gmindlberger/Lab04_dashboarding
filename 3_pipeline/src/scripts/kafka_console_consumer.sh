#!/bin/sh
CONTAINER_NAME="kafka"
TOPIC_NAME="weather-data-pipeline"
KAFKA_HOST="kafka:9092"

docker exec -it ${CONTAINER_NAME} \
    kafka-console-consumer.sh --bootstrap-server ${KAFKA_HOST} --topic ${TOPIC_NAME} --from-beginning