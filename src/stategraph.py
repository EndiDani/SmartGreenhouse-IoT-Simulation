from langgraph.graph import StateGraph, START, END
from typing          import Annotated, TypedDict, List
from operator        import add
from zones.zone      import Zone

class State(TypedDict): 
    light: float
    themperature: float
    air_quality: float
    vent_on: bool
    pump_on: bool
    events: Annotated[List[str], add] # lista di eventi critici attivi


def subscribe_sensor_data(mqtt_manager): 
    topic = f"greenhouse/+/+/raw"
    mqtt_manager.subscribe(topic)


def route_sensor_data(graph, zone: Zone, sensor_type: str, payload: float): 
    print(f"Graph received -> Zone: {zone.get_name()}, Sensor: {sensor_type}, Payload: {payload}")



