from typing                  import Dict, List, Any
from sensors.sensor_base     import Sensor
from actuators.actuator_base import Actuator
from random                  import uniform

# TODO: aggiungere uno storico e un calcolo media

class Zone: 
    def __init__(self, name: str, sensors: List[Sensor], actuators: List[Actuator], state: Dict[str, Any], neighbors: List[str]):
        self.name      = name
        self.sensors   = sensors
        self.actuators = actuators
        self.state     = state
        self.neighbors = neighbors
        self.X_light   = uniform(0.,   4094.)
        self.X_co2     = uniform(400., 1600.)

    def add_sensor(self, sensor: Sensor): 
        self.sensors.append(sensor)
    
    def add_actuators(self, actuator: Actuator): 
        self.actuators.append(actuator)

    def add_neighbors(self, zone: str): 
        self.neighbors.append(zone)

    def collect_data(self): 
        for sensor in self.sensors: 
            self.state[sensor.get_id()] = sensor.get_state()
        
    def workflow(self): 
        self.X_light += uniform(-20., 20.)
        self.X_co2   += uniform(-20., 20.)

        # X_light -> light_sens -> temp_sens -> umidity_sens ==> pump -> energy
        #                              | ===> vent -> energy
        # X_CO2 -> air_sens ==> vent -> energy

    def get_state(self) -> Dict[str, Any]: 
        return self.state
