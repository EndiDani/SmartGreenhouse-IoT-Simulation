from common_interfaces        import BasicSensor
from factories.sensor_factory import register_sensor


@register_sensor("energy_consume")
class EnergyConsumeSensor(BasicSensor): 
    def __init__(self): 
        self.idle_power = 6.3 # Watt
        self.state      = 0.
    
    def receive_data(self, received_data: float):
        self.state = received_data

    def get_state(self) -> float: 
        return self.state + self.idle_power

    def get_sensortype(self) -> str: 
        return "energy_consume"
    