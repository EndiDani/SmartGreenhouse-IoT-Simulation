from typing             import Dict, List
from sensors.sensor     import Sensor
from actuators.actuator import Actuator
from random             import uniform

# TODO: aggiungere calcolo media, max, min, ecc..

class Zone: 
    def __init__(self, name: str, sensors: List[Sensor], actuators: List[Actuator], neighbors: List[str]):
        self.name      = name
        self.neighbors = neighbors
        self.X_light   = 0.
        self.X_co2     = uniform(400., 1500.)

        self._validate_env(sensors, actuators)
        self._create_sensor_dict(sensors)
        self._create_state_dict(sensors)
        self._create_actuator_dict(actuators)
    
    def _validate_env(self, sensors: List[Sensor], actuators: List[Actuator]): 
        necessary_sensors = {"light", "thermometer", "air_quality", "humidity", "energy_consume"}
        sensor_types      = {sensor.get_sensortype() for sensor in sensors}
        missing_sensors   = necessary_sensors - sensor_types

        if missing_sensors:
            raise ValueError(f"Zone {self.name} missing sensors: {', '.join(missing_sensors)}")
        
        necessary_actuators = {"vent", "pump"}
        actuator_types      = {actuator.get_actuatortype() for actuator in actuators}
        missing_actuators   = necessary_actuators - actuator_types

        if missing_actuators: 
            raise ValueError(f"Zone {self.name} missing actuators: {', '.join(missing_actuators)}")

    def _create_sensor_dict(self, sensors: List[Sensor]):
        self.sensors: Dict[str, Sensor] = {}
        for sensor in sensors:
            self.sensors[sensor.get_sensortype()] = sensor

    def _create_actuator_dict(self, actuators: List[Actuator]): 
        self.actuators: Dict[str, Actuator] = {}
        for actuator in actuators: 
            self.actuators[actuator.get_actuatortype()] = actuator

    def _create_state_dict(self, sensors: List[Sensor]):
        self.state: Dict[str, List[float]] = {}
        for sensor in sensors: 
            self.state[sensor.get_sensortype()] = []

    def add_sensor(self, sensor: Sensor): 
        if sensor.get_sensortype() not in self.sensors: 
            self.sensors[sensor.get_sensortype()] = sensor
    
    def add_actuators(self, actuator: Actuator): 
        if actuator.get_actuatortype() not in self.actuators: 
            self.actuators[actuator.get_actuatortype()] = actuator

    def add_neighbors(self, zone: str): 
        if zone not in self.neighbors:
            self.neighbors.append(zone)

    def collect_data(self): 
        for name, sensor in self.sensors.items(): 
            self.state[name].append(sensor.get_state()) 

    def publish_sensor_data(self, mqtt_manager): 
        self.collect_data() # Li salvo per avere uno storico
        for name, sensor in self.sensors.items():
            topic = f"greenhouse/{self.name}/{name}/raw"
            mqtt_manager.publish(topic, sensor.get_state())

    def update_light(self, received_data: float):
        self.sensors["light"].receive_data(received_data)

    def update_thermometer(self, received_data: float): 
        pass

    def update_air_quality(self, received_data: float): 
        pass

    def update_humidity(self, received_data: float): 
        pass

    def update_energy_consume(self, received_data: float): 
        pass

    def get_state(self) -> Dict[str, float]: 
        return {sensor_id: values[-1] for sensor_id, values in self.state.items()}
    
    def get_name(self) -> str: 
        return self.name
