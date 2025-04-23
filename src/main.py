from mqtt_manager    import MqttManager
from zones_generator import create_zones
from stategraph      import subscribe_sensor_data, graph
import json

from zones.zone import Zone

zones_map = create_zones()

# Serializzo zones_map
zones_data = {key: value.to_dict() for key, value in zones_map.items()}
with open("zones/zones_data.json", "w") as f:
    json.dump(zones_data, f, indent=4)

mqtt_manager = MqttManager(broker_address="localhost", broker_port=1883)
mqtt_manager.setup()

mqtt_manager.receive_graph(graph)
mqtt_manager.receive_zones_map(zones_map)
subscribe_sensor_data(mqtt_manager)

# Test
for i in range(3): 
    zones_map["A"].publish_sensor_data(mqtt_manager)
print("\n\n")

mqtt_manager.loop_forever()
mqtt_manager.disconnect()
