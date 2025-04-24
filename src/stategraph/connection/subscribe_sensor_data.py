def subscribe_sensor_data(mqtt_manager): 
    topic = f"greenhouse/+/+/raw"
    mqtt_manager.subscribe(topic)