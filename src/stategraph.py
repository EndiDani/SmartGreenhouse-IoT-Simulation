from langgraph.graph import StateGraph, START, END
from typing          import Annotated, TypedDict, List

class State(TypedDict): 
    light: float
    themperature: float
    humidity: float
    air_quality: float
    energy_consume: float
    vent_on: bool
    pump_on: bool
    events: List[str] # lista di eventi critici attivi
    
def subscribe_sensor_data(mqtt_manager): 
    topic = f"greenhouse/+/+/raw"
    mqtt_manager.subscribe(topic)

def route_sensor_data(zones_map, zone, sensor_type, payload): 
    print(f"Graph received -> Zone: {zone}, Sensor: {sensor_type}, Payload: {payload}")
    match(sensor_type): 
        case "light": 
            light_handler(zones_map, zone, payload)
        case "thermometer": 
            themperature_handler(zones_map, zone, payload)
        case "air_quality": 
            air_quality_handler(zones_map, zone, payload)
        case "humidity": 
            humidity_handler(zones_map, zone, payload)
        case "energy_consume": 
            energy_handler(zones_map, zone, payload)
        case _: 
            print(f"Unknown sensor type: {sensor_type}")

def light_handler(zones_map, zone, value): 
    zones_map[zone].update_light(value)

def themperature_handler(zones_map, zone, value): 
    zones_map[zone].update_thermometer(value)   

def air_quality_handler(zones_map, zone, value): 
    zones_map[zone].update_air_quality(value) 

def humidity_handler(zones_map, zone, value): 
    zones_map[zone].update_humidity(value) 

def energy_handler(zones_map, zone, value): 
    zones_map[zone].update_energy_consume(value) 


graph_builder = StateGraph(State)
 