# NOTE: The container needs to share the same network to access kafka:9092 -> see network-definition in kafka compose
docker run `
    -e WEATHER_LOCATION_LAT=47.72 `
    -e WEATHER_LOCATION_LONG=13.09 `
    -e WEATHER_FORECAST_DAYS=4 `
    -e KAFKA_BROKER=kafka:9092 `
    -e KAFKA_TOPIC=weather-data-pipeline `
    --network lab-network `
    weather_data_producer