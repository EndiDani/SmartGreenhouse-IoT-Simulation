from langgraph.graph             import StateGraph, START, END
from typing                      import Annotated, TypedDict, List, Dict
from operator                    import add
from zones.zone                  import Zone
from langgraph.checkpoint.memory import MemorySaver
import json

class State(TypedDict): 
    zone:             str
    light:            float
    thermometer:      float
    delta_temp:       float
    air_quality:      float
    humidity:         float
    evaporation_rate: float
    energy_consume:   float
    vent_on:          bool
    pump_on:          bool
    env:              Dict[str, float]
    events:           Annotated[List[str], add] # lista di eventi critici attivi
    payload:          float
    type:             str


def load_zones_data(zone_name: str) -> dict: 
    with open("src/zones/zones_data.json", "r") as f: 
        zones_data = json.load(f)

    if zone_name not in zones_data: 
        raise ValueError(f"[Error exception] {zone_name} is not a valid zone name")
    
    zone = zones_data[zone_name]
    return zone


def build_initial_state(zone_name: str) -> dict: 
    zones_data = load_zones_data(zone_name)
    sensors    = zones_data["sensors"]
    actuators  = zones_data["actuators"]

    initial_state = {
        "zone":             zones_data["name"],
        "light":            sensors["light"]["state"],
        "thermometer":      sensors["thermometer"]["state"],
        "delta_temp":       0., 
        "air_quality":      sensors["air_quality"]["state"],
        "humidity":         sensors["humidity"]["state"],
        "evaporation_rate": 0., 
        "energy_consume":   sensors["energy_consume"]["state"],
        "vent_on":          actuators["vent"]["powered"],
        "pump_on":          actuators["pump"]["powered"],
        "env": {
            # Termometro
            "k_temp":                 sensors["thermometer"]["k"],
            "min_temp":               sensors["thermometer"]["min_temp"],
            "max_temp":               sensors["thermometer"]["max_temp"],
            "k_fan_temp":             sensors["thermometer"]["k_fan"],
            "act_threshold_temp":     sensors["thermometer"]["act_threshold"],
            # Umidità
            "min_hum":                sensors["humidity"]["min_hum"],
            "max_hum":                sensors["humidity"]["max_hum"],
            "evap_coeff":             sensors["humidity"]["evap_coeff"],
            "evap_offset":            sensors["humidity"]["evap_offset"],
            "pump_gain":              sensors["humidity"]["pump_gain"],
            "act_threshold_humidity": sensors["humidity"]["act_threshold"],
            # Qualità aria
            "min_ppm":                sensors["air_quality"]["min_ppm"],
            "max_ppm":                sensors["air_quality"]["max_ppm"],
            "k_air":                  sensors["air_quality"]["k"],
            "k_fan_air":              sensors["air_quality"]["k_fan"],
            "act_threshold_air":      sensors["air_quality"]["act_threshold"],
            # Energia
            "idle_power":             sensors["energy_consume"]["idle_power"],
            # Ventola
            "power_rating_vent":      actuators["vent"]["power_rating"],
            # Pompa
            "power_rating_pump":      actuators["pump"]["power_rating"]
        },
        "events": [],
    }
    return initial_state


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
        previous_state = build_initial_state(zone.get_name())
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
        case "air_quality":
            print("[Router] Routing to: on_air_quality_data")
            return "on_air_quality_data"
        case _:
            return END

# -- Percorso sensore luce --
def on_light_data(state: State) -> State:
    payload = state.pop("payload", None)
    state["light"] = payload 
    print(f"\n[on_light_data] Updated light to {state['light']}\n")
    return state

def on_air_quality_data(state: State) -> State:
    payload = state.pop("payload", None)
    state["air_quality"] = payload
    print(f"\n[on_air_quality_data] Updated air_quality to {state['air_quality']}\n")
    return state

# Δtemp = ( ΔLuminosità / 10 ) * k 
def compute_new_temperature(state: State) -> State: 
    state["delta_temp"] = state["light"] / 10 * state["env"]["k_temp"]
    state["thermometer"] += state["delta_temp"]
    print(f"[compute_new_temperature] Updated thermometer to {state['thermometer']}\n")
    return state

# Δumidità = evap_coeff * temp - evap_offset 
def compute_new_humidity(state: State) -> State:
    rate = state["env"]["evap_coeff"] * state["thermometer"] - state["env"]["evap_offset"]
    state["evaporation_rate"] = max(rate, 0.0)
    state["humidity"] -= state["evaporation_rate"]
    print(f"[compute_new_humidity] Updated humidity to {state['humidity']}\n")
    return state

def is_pump_on(state: State): 
    if state["pump_on"]:
        print(f"[is_pump_on] Routing to: actuate_pump\n")
        return "actuate_pump"
    else:
        print(f"[is_pump_on] Routing to: need_pump_for_humidity (check)\n")
        return "need_pump_for_humidity"

def is_vent_on(state: State): 
    if state["vent_on"]: 
        print(f"[is_vent_on] Routing to: actuate_vent\n")
        return "actuate_vent"
    # Devo spedirlo sia per air quality
    # Che per temperature
    #

def need_pump_for_humidity(state: State) -> State: 
    humidity = state["humidity"]
    min_allowed = state["env"]["min_hum"]

    humidity_safe_range = humidity > min_allowed
    state["pump_on"] = not humidity_safe_range
    print(f"[need_pump_for_humidity] Check completed, pump is in {state['pump_on']}\n")
    return state

def need_vent_for_air_quality(state: State) -> State: 
    air_quality = state["air_quality"]
    max_allowed = state["env"]["max_ppm"]
    
    air_in_safe_range = air_quality < max_allowed
    state["vent_on"] = not air_in_safe_range
    print(f"[need_vent_for_air_quality] Check completed, vent is in {state['vent_on']}\n")
    return state

def need_vent_for_temperature(state: State) -> State:
    temp = state["thermometer"]
    max_allowed = state["env"]["max_temp"]
    
    temp_in_safe_range = temp < max_allowed
    state["vent_on"] = not temp_in_safe_range
    print(f"[need_vent_for_temperature] Check completed, vent is in {state['vent_on']}\n")
    return state

def actuate_vent(state: State) -> State: 
    # Termometro:
    delta_actuator = state["delta_temp"] * state["env"]["k_fan_temp"]
    state["thermometer"] -= delta_actuator
    check_temp = state["thermometer"] < state["env"]["act_threshold_temp"]
    
    # Qualita aria: 
    delta_actuator = -state["env"]["k_fan_air"] * state["air_quality"]
    state["air_quality"] -= delta_actuator
    check_air_quality = state["air_quality"] > state["act_threshold_air"]

    # Controllo ventola
    state["vent_on"] = check_temp or check_air_quality
    print(f"[actuate_vent] Actuation completed:\nVent: {state['vent_on']}\nTemp: {state['thermometer']}\nAir quality: {state['air_quality']}\n")
    return state

def actuate_pump(state: State) -> State: 
    net_gain = state["env"]["pump_gain"] - state["evaporation_rate"]
    state["humidity"] += net_gain
    state["pump_on"] = state["humidity"] < state["env"]["act_threshold_humidity"]
    print(f"[actuate_pump] Actuation completed:\nPump: {state['pump_on']}\nHumidity: {state['humidity']}\n")
    return state

def compute_energy_consume(state: State) -> State: 
    energy_consume = state["env"]["idle_power"]
    if state["vent_on"]: 
        energy_consume += state["env"]["power_rating_vent"]
    if state["pump_on"]: 
        energy_consume += state["env"]["power_rating_pump"]

    state["energy_consume"] = energy_consume
    print(f"[compute_energy_consume] Energy consumed: {state['energy_consume']}\n\n")
    return state


graph_builder = StateGraph(State)

# graph_builder.add_node("router_node", router_node)

graph_builder.add_node("on_light_data", on_light_data)
graph_builder.add_node("on_air_quality_data", on_air_quality_data)


# graph_builder.add_edge(START, "router_node")
graph_builder.add_conditional_edges(START, router_node)

graph_builder.add_edge("on_light_data", END)
graph_builder.add_edge("on_air_quality_data", END)

# Implementa memory saver + thread nel main
checkpointer = MemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)



'''
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
'''