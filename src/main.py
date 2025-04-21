from mqtt_manager    import MqttManager
from zones_generator import create_zones

zones = create_zones()

mqtt_manager = MqttManager(broker_address="localhost", broker_port=1883)
mqtt_manager.setup()

zones[1].workflow()
zones[1].publish_sensor_data(mqtt_manager)

# mqtt_manager.subscribe("test/topic")
# mqtt_manager.publish("test/topic", "Hello MQTT")

mqtt_manager.loop_forever()
mqtt_manager.disconnect()