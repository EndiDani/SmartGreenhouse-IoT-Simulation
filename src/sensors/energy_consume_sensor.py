from common_interfaces        import SensorType
from factories.sensor_factory import register_sensor


@register_sensor("energy_consume")
class EnergyConsumeSensor(SensorType): 
    def __init__(self): 
        self.idle_power = 6.3 # Watt
        self.state      = self.idle_power
    
    def receive_data(self, received_data: float):
        self.state += received_data
        # I dati ricevuti saranno il consumo energetico degli attuatori

    def check_state(self) -> bool:
        return False
    
    def actuator_on(self, actuator_on: bool) -> bool: 
        if not actuator_on: 
            self.state = self.idle_power

    def get_state(self) -> float: 
        return self.state

    def get_sensortype(self) -> str: 
        return "energy_consume"
    