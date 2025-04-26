from   zones.zone                           import Zone
from   stategraph.state.build_initial_state import build_initial_state

# Traccia stati inizializzati
initialized_states = {}

async def route_sensor_data(graph, zone: Zone, sensor_type: str, payload: float): 
    print("\n------ ------ ------ ------ ------ ------")
    print(f"\nGraph received -> Zone: {zone.get_name()}, Sensor: {sensor_type}, Payload: {payload}")

    thread_id = zone.get_name()
    config = {"configurable": {"thread_id": thread_id}}

    # Inizializzo o recupero lo stato
    if thread_id not in initialized_states:
        print(f"[INFO] State not found for {thread_id}, initializing a new state.")
        previous_state = build_initial_state(zone.get_name())
        initialized_states[thread_id] = previous_state
    else:
        previous_state = graph.get_state(config).values
        print(f"[INFO] Loaded previous state, starting with topic: {sensor_type}\n")

    # Aggiornamento stato con i valori nuoivi
    previous_state["type"] = sensor_type
    previous_state["payload"] = payload

    await graph.ainvoke(
        previous_state,
        config,
        stream_mode="values"
    )