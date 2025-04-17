from typing                  import Dict, List, Any
from sensors.sensor_base     import Sensor
from actuators.actuator_base import Actuator

class Zone: 
    def __init__(self, name: str, sensors: List[Sensor], actuators: List[Actuator], state: Dict[str, Any], neighbors: List[str]):
        self.name = name
        self.sensors = sensors
        self.actuators = actuators
        self.state = state
        self.neighbors = neighbors

    def add_sensor(self, sensor: Sensor): 
        self.sensors.append(sensor)
    
    def add_actuators(self, actuator: Actuator): 
        self.actuators.append(actuator)

    def add_neighbors(self, zone: str): 
        self.neighbors.append(zone)

    def collect_data(self): 
        for sensor in self.sensors: 
            self.state[sensor.get_id()] = sensor.get_state()
        
    def activate_actuator(self): 
        for sensor in self.sensors: 
            pass

    def get_state(self) -> Dict[str, Any]: 
        return self.state
    

        