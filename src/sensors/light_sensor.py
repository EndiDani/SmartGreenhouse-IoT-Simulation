from common_interfaces        import SensorType
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("light")
class LightSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(0., 4094.))

    def receive_data(self, received_data: float):
        # Questo puo essere inteso come un aumento di luce da fonti esterne al sensore
        # quindi un aumento non dipendente da altri sensori
        self.values.append(self.values[-1] + received_data)

    def check_state(self) -> bool:
        # TODO: In futuro si potrebbbe pensare a un attuatore "tenda" per 
        # sopprimere la luce eccessiva
        # per ora il sensore non comunicherà nulla su cui agire
        return False       

    def get_state(self) -> float: 
        return self.values[-1]
    
    # def actuator_on(self, actuator_on: bool) -> bool: ===> tenda 
