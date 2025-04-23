from langgraph.graph             import StateGraph, START, END
from typing                      import Annotated, TypedDict, List
from operator                    import add
from zones.zone                  import Zone
from langgraph.checkpoint.memory import MemorySaver
import json

class State(TypedDict): 
    type: str
    payload: float
    zone: str
    light: float
    temperature: float
    air_quality: float
    vent_on: bool
    pump_on: bool
    events: Annotated[List[str], add] # lista di eventi critici attivi


def load_zone(zone_name: str) -> Zone: 
    with open("zones/zones_data.json", "r") as f: 
        zones_data = json.load(f)
    
    if zone_name not in zones_data: 
        raise ValueError(f"[Error exception] {zone_name} is not a valid zone name")
    
    zone = zones_data[zone_name]
    return Zone.from_dict(zone)

def save_zone(zone: Zone): 
    with open("zones/zones_data.json", "r") as f:
        zones_data = json.load(f)
    
    zones_data[zone.get_name()] = zone.to_dict()
    
    with open("zones/zones_data.json", "w") as f:
        json.dump(zones_data, f, indent=4)

def subscribe_sensor_data(mqtt_manager): 
    topic = f"greenhouse/+/+/raw"
    mqtt_manager.subscribe(topic)


def route_sensor_data(graph, zone: Zone, sensor_type: str, payload: float): 
    print(f"Graph received -> Zone: {zone.get_name()}, Sensor: {sensor_type}, Payload: {payload}")

    thread_id = zone.get_name()
    config = {"configurable": {"thread_id": thread_id}}
    previous_state = graph.get_state(config).values

    # Recupero lo stato (se non è la prima volta)
    if not previous_state:
        print(f"[INFO] Stato non trovato per zona {thread_id}, inizializzo nuovo stato.")
        previous_state = {
            "zone": thread_id,
            "light": 0.0,
            "temperature": 0.0,
            "air_quality": 0.0,
            "vent_on": False,
            "pump_on": False,
            "events": [],
        }
    else:
        print(f"[INFO] Stato recuperato per zona {thread_id}: {previous_state}")

    # Aggiornamento stato con i valori nuoivi
    previous_state["type"] = sensor_type
    previous_state["payload"] = payload

    graph.invoke(
        previous_state,
        config,
        stream_mode="values"
    )


def router_node(state: State):
    # tolgo 'type' dallo state
    type = state.pop("type", None) 
    match type:
        case "light":
            print("[Router] Routing to: on_light_data")
            return "on_light_data"
        case "thermometer":
            print("[Router] Routing to: on_temperature_data")
            return "on_temperature_data"
        case "air_quality":
            print("[Router] Routing to: on_air_quality_data")
            return "on_air_quality_data"
        case _:
            return END

        
def on_light_data(state: State) -> State:
    payload = state.pop("payload", None)
    state["light"] += payload 
    print(f"[on_light_data] Updated light to {state['light']}\n")
    return state

def on_temperature_data(state: State) -> State:
    payload = state.pop("payload", None)
    state["temperature"] = payload
    print(f"[on_temperature_data] Updated temperature to {state['temperature']}\n")
    return state

def on_air_quality_data(state: State) -> State:
    payload = state.pop("payload", None)
    state["air_quality"] = payload
    print(f"[on_air_quality_data] Updated air_quality to {state['air_quality']}\n")
    return state


graph_builder = StateGraph(State)

# graph_builder.add_node("router_node", router_node)

graph_builder.add_node("on_light_data", on_light_data)
graph_builder.add_node("on_temperature_data", on_temperature_data)
graph_builder.add_node("on_air_quality_data", on_air_quality_data)


# graph_builder.add_edge(START, "router_node")
graph_builder.add_conditional_edges(START, router_node)

graph_builder.add_edge("on_light_data", END)
graph_builder.add_edge("on_temperature_data", END)
graph_builder.add_edge("on_air_quality_data", END)

# Implementa memory saver + thread nel main
checkpointer = MemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)