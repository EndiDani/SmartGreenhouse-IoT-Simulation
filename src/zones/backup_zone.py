from typing             import Dict, List
from sensors.sensor     import Sensor
from actuators.actuator import Actuator
from random             import uniform


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
    
    # TODO: estendere la possibilita che un sensore gestisca piu attuatori
    def _actuator_policy(self, sensors: List[str]): 
        policies = {
            "thermometer": "vent",
            "air_quality": "vent", 
            "humidity":    "pump"
        }

        actuator = {policies[sensor] for sensor in sensors}
        if len(actuator) != 1: 
            raise ValueError(
                f"Inconsistent actuator policy among sensors (actuactuators must be equal): {sensors} : {actuator}"
            )
        actuator = actuator.pop()

        maintenance_check = all(
            self.sensors[sensor_name].check_state() 
            for sensor_name in sensors
        )

        if maintenance_check and not self.actuators[actuator].is_on(): 
            self.actuators[actuator].switch()
        
        if self._is_needed(actuator, sensors): 
            self.actuators[actuator].switch()
    
    def _update_raw(self): 
        self.X_light = uniform(-20., 20.)

        delta_co2 = uniform(-20., 20.)
        self.X_co2   += delta_co2

    # TODO: implementare calo realistico della luce rilevato da thermoter che fa scendere la temp
    def _handle_light_air_temperature(self): 
        self.sensors["light"].receive_data(self.X_light)
        self.sensors["air_quality"].receive_data(self.X_co2)
        self.sensors["thermometer"].receive_data(self.X_light)
    
    def _handle_ventilation(self): 
        self._actuator_policy(["thermometer", "air_quality"])

    def _handle_humidity_pump(self):
        self.sensors["humidity"].receive_data(self.sensors["thermometer"].get_state())
        self._actuator_policy(["humidity"])
    
    def _collect_energy(self): 
        self.sensors["energy_consume"].receive_data(self._energy_calculation())

    def workflow(self): 
        self._update_raw()
        self._handle_light_air_temperature()
        self._handle_ventilation()
        self._handle_humidity_pump()
        self._collect_energy()
        self.collect_data()        
        # self.publish_sensor_data() 

    def get_state(self) -> Dict[str, float]: 
        return {sensor_id: values[-1] for sensor_id, values in self.state.items()}
    
    def get_name(self) -> str: 
        return self.name

# MQTT: implementazione
    def publish_sensor_data(self, mqtt_manager): 
        for name, sensor in self.sensors.items():
            topic = f"greenhouse/{self.name}/{name}"
            mqtt_manager.publish(topic, sensor.get_state())

# # # # # # #
# Workflow
    # X_light -> light_sens -> temp_sens -> umidity_sens ==> pump -> energy
    #                              | ->         ===>         vent -> energy
    # X_CO2      ->    air_sens      ===>       ===>         vent -> energy
