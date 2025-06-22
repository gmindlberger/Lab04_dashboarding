$containerName = "kafka"
$topicName = "weather-data-pipeline"
$kafkaHost = "kafka:9092"

docker exec -it $containerName `
  kafka-topics.sh --create `
  --bootstrap-server $kafkaHost `
  --topic $topicName `
  --partitions 1 `
  --replication-factor 1