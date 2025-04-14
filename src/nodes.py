from random import uniform
from typing import Dict, List, Tuple


class Node(): 
    def __init__(self, id: str, sensor_type: str): 
        self.id = id
        self.sensor_type = sensor_type
        self.data_generator()
    
    def data_generator(self): 
        match self.sensor_type: 
            case "thermometer": 
                self.state = uniform(15., 35.)

            case "humidity": 
                self.state = uniform(30., 90.)
            
            case "air_quality": 
                self.state = uniform(10., 150.)
            
            case "brightness": 
                self.state = uniform(0., 100.)

            case _: 
                self.state = uniform(0., 99.)

    def send_data(self): 
        return self.id, self.sensor_type, self.state

    def print_data(self): 
        print(f"Sensor: {self.id} ({self.sensor_type}), State: {self.state}")

    def receive_data(self, received_data: float): 
        # Sensor logic to add when it receives data
        print(f"Sensor: {self.id} ({self.sensor_type}), Received: {received_data}")

    def get_state(self): 
        return self.state
    
    def get_id(self): 
        return self.id


class Broker(): 
    def __init__(self): 
        self.topic_data: Dict[str, List] = {}
        self.topic_subscribed: Dict[str, List] = {}

    def receive_data(self, received: Tuple[str, str, float]): 
        id    = received[0]
        topic = received[1]
        data  = received[2]

        if topic not in self.topic_subscribed: 
            print("The device is not registered in any topic.")
            return 
        
        self.topic_data[topic].append(data)
        self.publish(topic, id)

    def publish(self, topic: str, id: str): 
        sensors = [sensor for sensor in self.topic_subscribed[topic] if sensor.get_id() != id]
        
        if sensors: 
            for sensor in sensors: 
                sensor.receive_data(self.topic_data[topic][-1])
                
    def subscribe(self, topic: str, node: Node): 
        if topic not in self.topic_subscribed: 
            self.topic_subscribed[topic] = []
            self.topic_data[topic] = []

        self.topic_subscribed[topic].append(node)
        self.topic_data[topic].append(node.get_state())


# # #

print("")
thermometer = Node("UltraTermo", "thermometer")
water_heater = Node("Heater01x", "thermometer")

thermometer.print_data()
water_heater.print_data()
print("")

broker = Broker()
broker.subscribe("thermometer", thermometer)
broker.subscribe("thermometer", water_heater)
broker.receive_data(thermometer.send_data())

