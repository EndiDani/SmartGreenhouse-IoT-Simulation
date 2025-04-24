import json
import os

def load_zones_data(zone_name: str) -> dict: 
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    zones_data_path = os.path.join(BASE_DIR, 'zones', 'zones_data.json')

    with open(zones_data_path, "r") as f: 
        zones_data = json.load(f)

    if zone_name not in zones_data: 
        raise ValueError(f"[Error exception] {zone_name} is not a valid zone name")
    
    zone = zones_data[zone_name]
    return zone
