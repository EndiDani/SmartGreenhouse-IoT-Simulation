from common_interfaces        import BasicSensor
from factories.sensor_factory import register_sensor

# TODO: implementare attuatore 'tenda' per controllare la luce

@register_sensor("light")
class LightSensor(BasicSensor): 
    def __init__(self): 
        self.state = 1000.

    def receive_data(self, received_data: float):
        self.state += received_data
    
    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "light"
