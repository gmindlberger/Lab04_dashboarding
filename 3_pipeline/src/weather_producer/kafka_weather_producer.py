import json
import os
import sys

import requests
from confluent_kafka import Producer


# Function to fetch weather data
def fetch_weather_data(lat, long, forecast_days):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': long,
        'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m',
        'timezone': 'UTC',
        'forecast_days': forecast_days  # look into the future
    }
    response = requests.get(url, params=params)
    return response.json()


# take the fetched weather-data and publish it to a given Kafka topic
def publish_to_kafka(weather_data, kafka_broker, kafka_topic):

    # Callback to confirm delivery
    def delivery_report(err, msg):
        if err is not None:
            print(f"Delivery failed: {err}")
        else:
            print(f"Sent: {msg.value().decode('utf-8')}")

    producer = Producer({'bootstrap.servers': kafka_broker})
    hourly_data = weather_data['hourly']
    for i, timestamp in enumerate(hourly_data['time']):
        record = {
            'timestamp': timestamp,
            'temperature': hourly_data['temperature_2m'][i],
            'humidity': hourly_data['relative_humidity_2m'][i],
            'wind_speed': hourly_data['wind_speed_10m'][i]
        }
        payload = json.dumps(record).encode('utf-8')
        producer.produce(kafka_topic, value=payload, callback=delivery_report)
        producer.poll(0)  # Trigger delivery report callbacks

    producer.flush()


# get the given key from the environment or use default value
def get_env_default(key: str, default_val: str) -> str:
    val = os.environ.get(key)
    if val is None or val == "":
        return default_val
    return val


def main():
    # Location: Puch-Urstein
    lat = get_env_default("WEATHER_LOCATION_LAT", "47.72")
    long = get_env_default("WEATHER_LOCATION_LONG", "13.09")
    forecast_days = get_env_default("WEATHER_FORECAST_DAYS", 4)
    # see listener configuration @ kafka
    kafka_broker = get_env_default("KAFKA_BROKER", "localhost:19092")
    kafka_topic = get_env_default("KAFKA_TOPIC", "weather-data-pipeline")

    weather_data = fetch_weather_data(lat, long, forecast_days)
    if weather_data is None:
        print("Could not get weather-data!")
        sys.exit(2)

    publish_to_kafka(weather_data=weather_data,
                     kafka_broker=kafka_broker,
                     kafka_topic=kafka_topic)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as err:
        print(f"Got Error {err=}, {type(err)=}")
