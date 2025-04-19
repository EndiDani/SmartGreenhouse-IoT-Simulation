from typing             import Dict, List
from sensors.sensor     import Sensor
from actuators.actuator import Actuator
from random             import uniform

# TODO: aggiungere calcolo media, max, min, ecc..

class Zone: 
    def __init__(self, name: str, sensors: List[Sensor], actuators: List[Actuator], neighbors: List[str]):
        self.name      = name
        self.neighbors = neighbors
        self.X_light   = uniform(0.,   4094.)
        self.X_co2     = uniform(400., 1600.)
        self.state:      Dict[str, List[float]] = {}

        self._validate_env(sensors, actuators)
        self._create_sensor_dict(sensors)
        self._create_actuator_dict(actuators)
    
    def _validate_env(self, sensors: List[Sensor], actuators: List[Actuator]): 
        necessary_sensors = ["light", "thermometer", "air_quality", "humidity", "energy_consume"]
        sensor_types      = {sensor.get_sensortype() for sensor in sensors}
        missing_sensors   = necessary_sensors - sensor_types

        if missing_sensors:
            raise ValueError(f"Zone {self.name} missing sensors: {', '.join(missing_sensors)}")
        
        necessary_actuators = ["vent", "pump"]
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

    def add_sensor(self, sensor: Sensor): 
        self.sensors[sensor.get_sensortype] = sensor
    
    def add_actuators(self, actuator: Actuator): 
        self.actuators[actuator.get_actuatortype()] = actuator

    def add_neighbors(self, zone: str): 
        self.neighbors.append(zone)

    def collect_data(self): 
        for name, sensor in self.sensors.items(): 
            self.state[name].append(sensor.get_state()) 

    def _energy_calculation(self) -> float: 
        energy_consumed = 0.

        if self.actuators["pump"].is_on(): 
            energy_consumed += self.actuators["pump"].get_consume()
        
        if self.actuators["vent"].is_on(): 
            energy_consumed += self.actuators["vent"].get_consume()

        return energy_consumed
    
    def _is_needed(self, actuator: str, sensors: List[str]): 
        if self.actuators[actuator].is_on():
            return all(
                self.sensors[sensor_name].actuator_on() 
                for sensor_name in sensors
            )
        return False
    
    def _actuator_policy(self, sensors: List[str]): 
        policies = {
            "thermometer": "vent",
            "air_quality": "vent", 
            "humidity":    "pump"
        }

        actuator = {policies[sensor] for sensor in sensors}
        if len(actuator) != 1: 
            raise ValueError(f"Inconsistent actuator policy among sensors: {sensors} : {actuator}")

        maintenance_check = all(
            self.sensors[sensor_name].check_state() 
            for sensor_name in sensors
        )

        if maintenance_check and not self.actuators[actuator].is_on(): 
            self.actuators[actuator].switch()
        
        if self._is_needed(actuator, sensors): 
            self.actuators[actuator].switch()
    
    def _update_raw(self): 
        self.X_light += uniform(-20., 20.)
        self.X_co2   += uniform(-20., 20.)

    def _handle_light_air_temperature(self): 
        self.sensors["light"].receive_data(self.X_light)
        self.sensors["air_quality"].receive_data(self.X_co2)
        self.sensors["thermometer"].receive_data(self.sensors["light"].get_state())
    
    def _handle_ventilation(self): 
        maintenance_check = self.sensors["thermometer"].check_state() or self.sensors["air_quality"].check_state()

        if maintenance_check and not self.actuators["vent"].is_on():
            self.actuators["vent"].switch()
        
        if self._is_needed(actuator="vent", sensors=["thermometer", "air_quality"]):
            self.actuators["vent"].switch()

    def _handle_humidity_pump(self):
        self.sensors["humidity"].receive_data(self.sensors["thermometer"].get_state())

        maintenance_check = self.sensors["humidity"].check_state() 

        if maintenance_check and not self.actuators["pump"].is_on():
            self.actuators["pump"].switch()

        if self._is_needed(actuator="pump", sensors=["humidity"]):
            self.actuators["pump"].switch()
    
    def _collect_energy(self): 
        self.sensors["energy_consume"].receive_data(self._energy_calculation())

    def workflow(self): 
        self._update_raw()
        self._handle_light_air_temperature()
        self._handle_ventilation()
        self._handle_humidity_pump()
        self._collect_energy()
        self.collect_data()         

    def get_state(self) -> Dict[str, float]: 
        return {sensor_id: values[-1] for sensor_id, values in self.state.items()}


# Workflow
    # X_light -> light_sens -> temp_sens -> umidity_sens ==> pump -> energy
    #                              | ->         ===>         vent -> energy
    # X_CO2      ->    air_sens      ===>       ===>         vent -> energy
