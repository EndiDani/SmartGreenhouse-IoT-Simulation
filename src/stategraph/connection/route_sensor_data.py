from   zones.zone                           import Zone
from   stategraph.state.build_initial_state import build_initial_state
import asyncio

async def route_sensor_data(graph, zone: Zone, sensor_type: str, payload: float): 
    print(f"Graph received -> Zone: {zone.get_name()}, Sensor: {sensor_type}, Payload: {payload}")

    thread_id = zone.get_name()
    config = {"configurable": {"thread_id": thread_id}}
    previous_state = graph.get_state(config).values

    # Recupero lo stato (se non è la prima volta)
    if not previous_state:
        print(f"[INFO] Stato non trovato per zona {thread_id}, inizializzo nuovo stato.")
        previous_state = build_initial_state(zone.get_name())
    else:
        pass
        # print(f"[INFO] Stato recuperato per zona {thread_id}: {previous_state}")
        print(f"\n[INFO] Stato recuperato, inizio ciclo con topic: {sensor_type}")

    # Aggiornamento stato con i valori nuoivi
    previous_state["type"] = sensor_type
    previous_state["payload"] = payload

    await graph.ainvoke(
        previous_state,
        config,
        stream_mode="values"
    )