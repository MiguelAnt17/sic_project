import os
import time
import random
from kafka import KafkaProducer

MEAN_TEMP_DIFF = float(os.getenv("MEAN_TEMP_DIFF"))  
STD_DEV_TEMP_DIFF = float(os.getenv("STD_DEV_TEMP_DIFF")) 
KAFKA_BROKER = os.getenv("KAFKA_BROKER") 
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC") 
SENSOR_ID = os.getenv("SENSOR_ID")  


def generate_temp_diff():
    temp_diff = random.normalvariate(MEAN_TEMP_DIFF, STD_DEV_TEMP_DIFF)
    temp_diff = max(5, min(temp_diff, 20))  
    return temp_diff

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: v.encode('utf-8') 
)

def send_to_kafka(sensor_id, temp_diff):
    message = f"cooling_efficiency,sensor_id={sensor_id} value={temp_diff}"
    producer.send("cooling_efficiency_sensor", value=message)
    print(f"Sent to Kafka: {message}")

if __name__ == "__main__":
    try:
        while True:
            temp_diff = generate_temp_diff()
            send_to_kafka(SENSOR_ID, temp_diff)
            time.sleep(60) 
    except KeyboardInterrupt:
        print("Sensor stopped.")
    finally:
        producer.close()
