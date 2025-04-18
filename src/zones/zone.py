from typing                  import Dict, List
from sensors.sensor_base     import Sensor
from actuators.actuator_base import Actuator
from random                  import uniform

# TODO: aggiungere calcolo media, max, min, ecc..

class Zone: 
    def __init__(self, name: str, sensors: List[Sensor], actuators: List[Actuator], state: Dict[str, List[float]], neighbors: List[str]):
        self.name      = name
        self.actuators = actuators
        self.state     = state
        self.neighbors = neighbors
        self.X_light   = uniform(0.,   4094.)
        self.X_co2     = uniform(400., 1600.)
        self._create_sensor_dict(sensors)

    def _create_sensor_dict(self, sensors: List[Sensor]):
        self.sensors: Dict[str, Sensor] = {}
        for sensor in sensors:
            self.sensors[sensor.get_sensortype()] = sensor

    def _create_actuator_dict(self, actuators: List[Actuator]): 
        self.actuators: Dict[str, Actuator] = {}
        for actuator in actuators: 
            self.actuators[actuator.get_actuatortype()] = actuator

    def add_sensor(self, sensor: Sensor): 
        self.sensors.append(sensor)
    
    def add_actuators(self, actuator: Actuator): 
        self.actuators.append(actuator)

    def add_neighbors(self, zone: str): 
        self.neighbors.append(zone)

    def collect_data(self): 
        for name, sensor in self.sensors: 
            self.state[name].append(sensor.get_state()) ### TODO: SISTEMA DIZ
    
    def workflow(self): 
        self.X_light += uniform(-20., 20.)
        self.X_co2   += uniform(-20., 20.)

        self.sensors["light"].receive_data(self.X_light)
        self.sensors["air_quality"].receive_data(self.X_co2)
        self.sensors["thermometer"].receive_data(self.sensors["light"].get_state())

        maintenance_check = self.sensors["thermometer"].check_state() or self.sensors["air_quality"].check_state()

        if maintenance_check and not self.actuators["vent"].is_on():
            self.actuators["vent"].switch()
        
        if self.sensors["thermometer"].actuator_on(self.actuators["vent"].is_on()): 
            self.sensors["air_quality"].actuator_on(True)
            # L'ordine non importa, il ventilatore se è acceso per uno lo è anche per l'altro
        else: 
            self.actuators["vent"].switch()
            
        self.sensors["humidity"].receive_data(self.sensors["thermometer"].get_state())

        if self.sensors["humidity"].check_state() and not self.actuators["pump"].is_on():
            self.actuators["pump"].switch()

        if not self.sensors["humidity"].actuator_on(self.actuators["pump"].is_on()):
            self.actuators["pump"].switch()

        # calcolo energia consumata


        # X_light -> light_sens -> temp_sens -> umidity_sens ==> pump -> energy
        #                              | ===> vent -> energy
        # X_CO2 -> air_sens ==> vent -> energy

    def get_state(self) -> Dict[str, float]: 
        return {sensor_id: values[-1] for sensor_id, values in self.state.items()}
