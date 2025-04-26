from mqtt_manager                                import MqttManager
from zones_generator                             import create_zones
from stategraph.stategraph_builder               import build_stategraph
from stategraph.connection.subscribe_sensor_data import subscribe_sensor_data
import json 
import os

zones_map = create_zones()
# Serializzo zones_map
zones_data = {key: value.to_dict() for key, value in zones_map.items()}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
zones_data_path = os.path.join(BASE_DIR, 'zones', 'zones_data.json')

with open(zones_data_path, "w") as f:
    json.dump(zones_data, f, indent=4)


graph = build_stategraph()

mqtt_manager = MqttManager(broker_address="localhost", broker_port=1883)
mqtt_manager.start_async_loop()
mqtt_manager.setup()

mqtt_manager.receive_graph(graph)
mqtt_manager.receive_zones_map(zones_map)
subscribe_sensor_data(mqtt_manager)

# Test
for i in range(3): 
    for _, zone in zones_map.items():
        zone.publish_sensor_data(mqtt_manager)

mqtt_manager.loop_forever()
mqtt_manager.disconnect()
