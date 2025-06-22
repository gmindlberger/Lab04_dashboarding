$containerName = "kafka"
$topicName = "weather-data-pipeline"
$kafkaHost = "kafka:9092"

docker exec -it $containerName `
  kafka-console-consumer.sh --bootstrap-server $kafkaHost --topic $topicName --from-beginning