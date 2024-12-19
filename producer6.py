import os
import time
import random
from kafka import KafkaProducer

MEAN_HUMIDITY = float(os.getenv("MEAN_HUMIDITY"))   
STD_DEV_HUMIDITY = float(os.getenv("STD_DEV_HUMIDITY")) 
KAFKA_BROKER = os.getenv("KAFKA_BROKER")  
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC") 
SENSOR_ID = os.getenv("SENSOR_ID") 


def generate_humidity():
    humidity = random.normalvariate(MEAN_HUMIDITY, STD_DEV_HUMIDITY)
    humidity = max(0, min(humidity, 100)) 
    return humidity


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: v.encode('utf-8')  
)

def send_to_kafka(sensor_id, humidity):
    message = f"humidity,sensor_id={sensor_id} value={humidity}"
    producer.send("humidity_sensor", value=message)
    print(f"Sent to Kafka: {message}")

if __name__ == "__main__":
    try:
        while True:
            humidity = generate_humidity()
            send_to_kafka(SENSOR_ID, humidity)
            time.sleep(30)  
    except KeyboardInterrupt:
        print("Sensor stopped.")
    finally:
        producer.close()
