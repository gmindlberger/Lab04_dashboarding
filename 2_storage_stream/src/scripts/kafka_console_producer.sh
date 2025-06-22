#!/bin/sh
CONTAINER_NAME="kafka"
TOPIC_NAME="test-topic"
KAFKA_HOST="kafka:9092"

docker exec -it ${CONTAINER_NAME} \
  kafka-console-producer.sh --bootstrap-server ${KAFKA_HOST} --topic ${TOPIC_NAME}