import os
import time
import random
from kafka import KafkaProducer

MEAN_POWER = float(os.getenv("MEAN_POWER"))  
STD_DEV_POWER = float(os.getenv("STD_DEV_POWER")) 
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")  
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC") 
SENSOR_ID = os.getenv("SENSOR_ID") 


def generate_power_reading():
    power = random.normalvariate(MEAN_POWER, STD_DEV_POWER)
    power = max(100, min(power, 2000))  
    return power

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: v.encode('utf-8')  
)

def send_to_kafka(sensor_id, power):
    message = f"power,sensor_id={sensor_id} value={power}"
    producer.send("power_usage_sensor", value=message)
    print(f"Sent to Kafka: {message}")

if __name__ == "__main__":
    try:
        while True:
            power = generate_power_reading()
            send_to_kafka(SENSOR_ID, power)
            time.sleep(20)  
    except KeyboardInterrupt:
        print("Sensor stopped.")
    finally:
        producer.close()
