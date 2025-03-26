import time
import random
import json #python dictionaries need to be converted into a transmittable format.
import paho.mqtt.client as mqtt 
import uuid  # For generating client ID
import logging
logging.basicConfig(level=logging.DEBUG)
import os

cert_files = [
    "C:/Users/sithota/Downloads/AmazonRootCA1.pem",
    "C:/Users/sithota/Downloads/af0a460e9c150cad75d9346ed92556fa5e9c54366f9b66f97ca48678a8dc906a-certificate.pem.crt",
    "C:/Users/sithota/Downloads/af0a460e9c150cad75d9346ed92556fa5e9c54366f9b66f97ca48678a8dc906a-private.pem.key"
]

for f in cert_files:
    print(f"{f}: {'Exists' if os.path.exists(f) else 'Not found'}")


STATION_ID = "envstation1"
AWS_ENDPOINT = "a2h7qlfv6ja5e-ats.iot.us-east-2.amazonaws.com"
AWS_PORT = 8883
AWS_TOPIC = "environmental/station/" + STATION_ID
SIMULATION_MODE = False

# Base values that I set to get diverse simulatated data 
# of temp, humidity and co2 levels
base_temp = 24.0
base_humid = 40.0
base_co2_raw = 2000


def read_sensors():
    temp = base_temp + (random.random() * 2 - 1)   
    humid = base_humid + (random.random() * 4 - 2) 
    humid = max(0, min(100, humid))
    temp = max(-50, min(50, temp))
    # Simulate CO2 reading
    co2_raw = base_co2_raw + random.randint(-400, 400) 
    co2_raw = max(0, min(4095, co2_raw)) 
    co2_ppm = int((co2_raw / 4095) * 1700 + 300)  
    
    return {
        "temperature": round(temp, 1),
        "humidity": round(humid, 1),
        "co2": co2_ppm
    }

# Connect to MQTT (for AWS IoT connection)
def connect_mqtt():
    if SIMULATION_MODE: #i have used this to first simulate on pc and if it works
                        #then connect to aws
        print("SIMULATION MODE: MQTT connection simulated")
        return None
        
    try:
        # Create a client ID
        client_id = f'python-mqtt-{uuid.uuid4().hex}'
        # Create MQTT client
        client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
        # Set up TLS for secure connection
        client.tls_set(
    ca_certs="C:/Users/sithota/Downloads/AmazonRootCA1.pem", 
    certfile="C:/Users/sithota/Downloads/af0a460e9c150cad75d9346ed92556fa5e9c54366f9b66f97ca48678a8dc906a-certificate.pem.crt",
    keyfile="C:/Users/sithota/Downloads/af0a460e9c150cad75d9346ed92556fa5e9c54366f9b66f97ca48678a8dc906a-private.pem.key"
)

        
        # Connect to AWS IoT
        client.connect(AWS_ENDPOINT, port=AWS_PORT, keepalive=60)
        print("Connected to AWS IoT")
        client.loop_start()
        return client
    except Exception as e:
        print("Error connecting to AWS IoT:", e)
        return None

# Main program
def main():
    print("=== Environmental Monitoring Station ===")
    print(f"Station ID: {STATION_ID}")
    print("Reading sensors and publishing to AWS IoT...")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    mqtt_client = connect_mqtt()# Connect to MQTT
    historical_data = [] # Dictionary to store historical data

    # Main loop - read sensors and send data
    while True:
        # Read sensor values
        sensor_data = read_sensors()
        
        # Create timestamp
        timestamp = time.time()
        
        
        payload = {
            "station_id": STATION_ID,
            "timestamp": timestamp,
            "sensors": sensor_data
        }
        
        
        historical_data.append(payload)
        
        max_records = int(5 * 60 * 60 / 5)
        if len(historical_data) > max_records:
            historical_data = historical_data[-max_records:]
        
        # Convert to JSON
        json_payload = json.dumps(payload)
        
        # Print data to console
        print("-" * 40)
        print(f"Station ID: {STATION_ID}")
        print(f"Temperature: {sensor_data['temperature']}°C")
        print(f"Humidity: {sensor_data['humidity']}%")
        print(f"CO2: {sensor_data['co2']} ppm")
        print(f"JSON: {json_payload}")
        
        # Publish to MQTT if connected
        if mqtt_client:
            try:
                mqtt_client.publish(AWS_TOPIC, json_payload)
                print("Data published to AWS IoT")
            except Exception as e:
                print("Error publishing to AWS IoT:", e)
        else:
            print("SIMULATION MODE")
        
        display_latest_data(sensor_data)
        display_historical_data(historical_data, "temperature")
        display_historical_data(historical_data, "humidity")
        display_historical_data(historical_data, "co2")
        time.sleep(5)

# Function to display latest sensor data 
def display_latest_data(sensor_data):
    print("\n=== LATEST SENSOR DATA ===")
    print(f"Temperature: {sensor_data['temperature']}°C")
    print(f"Humidity: {sensor_data['humidity']}%")
    print(f"CO2: {sensor_data['co2']} ppm")
    print("==========================\n")

# Function to display historical data for a specific sensor
def display_historical_data(data_history, sensor_type):
    print(f"\n=== HISTORICAL DATA FOR {sensor_type.upper()} (LAST 5 HOURS) ===")
    for entry in data_history:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry["timestamp"]))
        value = entry["sensors"][sensor_type]
        print(f"{timestamp}: {value}")
    print("=======================================\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped by user")
    except Exception as e:
        print("Unexpected error:", e)