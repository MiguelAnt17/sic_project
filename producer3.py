import os
import time
import random
from kafka import KafkaProducer

MEAN_TEMPERATURE = float(os.getenv("MEAN_TEMP"))  
STD_DEV_TEMPERATURE = float(os.getenv("STD_DEV_TEMP"))
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")  
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC") 
SENSOR_ID = os.getenv("SENSOR_ID")  

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: v.encode('utf-8')  
)

def generate_temperature_reading():
    temperature = random.normalvariate(MEAN_TEMPERATURE, STD_DEV_TEMPERATURE)
    temperature = max(0, min(temperature, 30))  
    return temperature

def send_to_kafka(sensor_id, temperature):
    message = f"temperature,sensor_id={sensor_id} value={temperature}"
    producer.send("temperature_sensor", value=message)
    print(f"Sent to Kafka: {message}")

if __name__ == "__main__":
    try:
        while True:
            temperature = generate_temperature_reading()
            send_to_kafka(SENSOR_ID, temperature)
            time.sleep(30)  
    except KeyboardInterrupt:
        print("Sensor stopped.")
    finally:
        producer.close()
