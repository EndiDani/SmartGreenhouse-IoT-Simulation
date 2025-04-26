import json
import os
from mqtt_manager import MqttManager
from zones_generator import create_zones
from stategraph.stategraph_builder import build_stategraph
from stategraph.connection.subscribe_sensor_data import subscribe_sensor_data

# Configurazione del percorso per i dati delle zone
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZONES_DATA_PATH = os.path.join(BASE_DIR, 'zones', 'zones_data.json')

def save_zones_data(zones_map):
    """Serialize and save zone data to a JSON file."""
    zones_data = {key: value.to_dict() for key, value in zones_map.items()}
    with open(ZONES_DATA_PATH, "w") as f:
        json.dump(zones_data, f, indent=4)
    print(f"[INFO] Dati delle zone salvati in {ZONES_DATA_PATH}")

def initialize_mqtt_manager(graph, zones_map):
    """Initialize and configure the MQTT handler."""
    mqtt_manager = MqttManager(broker_address="localhost", broker_port=1883)
    mqtt_manager.start_async_loop()
    mqtt_manager.setup()
    mqtt_manager.receive_graph(graph)
    mqtt_manager.receive_zones_map(zones_map)
    subscribe_sensor_data(mqtt_manager)
    print("[INFO] MQTT Manager configurato e pronto.")
    return mqtt_manager

def run_test(mqtt_manager, zones_map, num_cycles = 3):
    """Runs a test by publishing sensor data for a specific number of cycles."""
    print(f"[INFO] Avvio del test con {num_cycles} cicli...")
    for cycle in range(1, num_cycles + 1):
        print(f"\n=== Ciclo {cycle}/{num_cycles} ===")
        for _, zone in zones_map.items():
            zone.publish_sensor_data(mqtt_manager)
    print("[INFO] Test completato.")

def main():
    # Creazione delle zone
    zones_map = create_zones()
    save_zones_data(zones_map)

    # Costruzione del grafo
    graph = build_stategraph()

    # Inizializzazione del gestore MQTT
    mqtt_manager = initialize_mqtt_manager(graph, zones_map)

    # Esecuzione del test
    try:
        run_test(mqtt_manager, zones_map)
        mqtt_manager.loop_forever()  # Mantiene il gestore MQTT attivo
    except KeyboardInterrupt:
        print("\n[INFO] Test interrotto dall'utente.")
    finally:
        mqtt_manager.disconnect()
        print("[INFO] MQTT Manager disconnesso.")

if __name__ == "__main__":
    main()