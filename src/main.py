from mqtt_manager    import MqttManager
from zones_generator import create_zones
from stategraph      import subscribe_sensor_data, graph

zones_map = create_zones()

mqtt_manager = MqttManager(broker_address="localhost", broker_port=1883)
mqtt_manager.setup()

mqtt_manager.receive_graph(graph)
mqtt_manager.receive_zones_map(zones_map)
subscribe_sensor_data(mqtt_manager)

zones_map["A"].publish_sensor_data(mqtt_manager)

mqtt_manager.loop_forever()
mqtt_manager.disconnect()