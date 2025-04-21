import paho.mqtt.client as mqtt
from   stategraph       import route_sensor_data

class MqttManager: 
    def __init__(self, broker_address, broker_port=1883, keep_alive_interval=60): 
        self.broker_address      = broker_address
        self.broker_port         = broker_port
        self.keep_alive_interval = keep_alive_interval
        self.client              = mqtt.Client()
    
    def receive_zones_map(self, zones_map): 
        self.zones_map = zones_map

    def on_connect(self, client, userdata, flags, rc): 
        if rc == 0: 
            print("Connected successfully to the broker")
        else: 
            print(f"Failed to connect with code {rc}")

    def on_message(self, client, userdata, msg): 
        topic_parts = msg.topic.split("/")
        if len(topic_parts) >= 4: 
            zone = topic_parts[1]
            sensor_type = topic_parts[2]
            payload = msg.payload.decode()

            # Conversione del payload in float
            try: 
                payload_value = float(payload)
                route_sensor_data(self.zones_map, zone, sensor_type, payload_value)
            except ValueError: 
                print(f"Error: Pyaload '{payload}' is not a valid number.")
        else: 
            print(f"Malformed topic: {msg.topic}")

    def on_publish(self, client, userdata, mid): 
        print(f"Message with mid {mid} has been succesfully published.")
    
    def on_disconnect(self, client, userdata, rc): 
        if rc != 0: 
            print(f"Disconnected with error code {rc}")
        else: 
            print("Disconnected cleanly")

    def setup(self): 
        try: 
            self.client.on_connect    = self.on_connect
            self.client.on_message    = self.on_message
            self.client.on_disconnect = self.on_disconnect
            self.client.on_publish    = self.on_publish

            print(f"Connecting to {self.broker_address}...")
            self.client.connect(
                self.broker_address, 
                self.broker_port, 
                self.keep_alive_interval
            )

            # Loop in un thread separato per gestire i messaggi
            # self.client.loop_start()
        except Exception as e: 
            print(f"An unexpected error occurred during setup: {e}")

    def publish(self, topic, message):
        try:
            result = self.client.publish(topic, message)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Message '{message}' sent to topic '{topic}'")
            else:
                print(f"Failed to publish message '{message}' to topic '{topic}'. Error code: {result.rc}")
        except Exception as e:
            print(f"Unexpected error while publishing to topic: {e}")

    def subscribe(self, topic): 
        try: 
            result, mid = self.client.subscribe(topic)
            if result == mqtt.MQTT_ERR_SUCCESS:
                print(f"Successfully subscribed to topic: {topic}")
            else:
                print(f"Failed to subscribe to topic: {topic}. Error code: {result}")
        except Exception as e: 
            print(f"Unexpected error while subscribing to topic: {e}")

    def disconnect(self): 
        try: 
            self.client.disconnect()
            print("Disconnected from broker")
        except Exception as e: 
            print(f"Unexpected error while disconnecting: {e}")
        
    def loop_forever(self): 
        try: 
            self.client.loop_forever()
            # Blocca il programma per ricevere i messaggi
        except KeyboardInterrupt: 
            print("Loop interrupted by user.")
        except Exception as e: 
            print(f"Unexpected error in loop: {e}")
        finally: 
            self.client.loop_stop()
            self.disconnect()