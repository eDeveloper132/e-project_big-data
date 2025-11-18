import csv
import json
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_RECORDS_CSV = 1000
NUM_RECORDS_JSON = 100
CSV_OUTPUT_FILE = 'dummy_climate_data.csv'
JSON_OUTPUT_FILE = 'sensor_data.json'
REGIONS = ['North', 'South', 'East', 'West']
START_DATE = datetime(2023, 1, 1)

# --- CSV Data Generation (Simulating Weather Stations) ---
def generate_csv_data():
    """Generates a CSV file with dummy climate data."""
    header = ['timestamp', 'region', 'temperature', 'humidity', 'pressure']
    
    with open(CSV_OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for i in range(NUM_RECORDS_CSV):
            timestamp = START_DATE + timedelta(days=i, hours=random.randint(0, 23))
            region = random.choice(REGIONS)
            
            # Simulate some missing data
            temperature = round(random.uniform(5.0, 35.0), 2) if random.random() > 0.05 else ''
            humidity = round(random.uniform(30.0, 90.0), 2) if random.random() > 0.05 else ''
            pressure = round(random.uniform(980.0, 1050.0), 2)
            
            writer.writerow([timestamp.isoformat(), region, temperature, humidity, pressure])
            
    print(f"Successfully generated {NUM_RECORDS_CSV} records in '{CSV_OUTPUT_FILE}'")


# --- JSON Data Generation (Simulating Real-time Sensor Streams) ---
def generate_json_data():
    """Generates a JSON file simulating sensor data streams."""
    data = []
    for _ in range(NUM_RECORDS_JSON):
        record = {
            "sensorId": f"sensor_{random.randint(1, 20)}",
            "timestamp": (START_DATE + timedelta(minutes=random.randint(0, 100000))).isoformat(),
            "reading": {
                "type": random.choice(["temperature", "humidity"]),
                "value": round(random.uniform(5.0, 35.0), 2)
            },
            "location": {
                "region": random.choice(REGIONS)
            }
        }
        data.append(record)
        
    with open(JSON_OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully generated {NUM_RECORDS_JSON} records in '{JSON_OUTPUT_FILE}'")


if __name__ == '__main__':
    generate_csv_data()
    generate_json_data()
