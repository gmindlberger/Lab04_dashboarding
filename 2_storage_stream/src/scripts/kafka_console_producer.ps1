$containerName = "kafka"
$topicName = "test-topic"
$kafkaHost = "kafka:9092"

docker exec -it $containerName `
  kafka-console-producer.sh --bootstrap-server $kafkaHost --topic $topicName