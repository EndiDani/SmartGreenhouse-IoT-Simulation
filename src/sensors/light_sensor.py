from common_interfaces        import BasicSensor
from factories.sensor_factory import register_sensor


@register_sensor("light")
class LightSensor(BasicSensor): 
    def __init__(self): 
        self.state = 0 
        # il valore sarà deciso dall'esterno

    def receive_data(self, received_data: float):
        self.state = received_data
        # Questo puo essere inteso come un aumento di luce da fonti esterne al sensore
        # quindi un aumento non dipendente da altri sensori
    
    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "light"
    
    # def check_state(self) -> bool:    
        # TODO: In futuro si potrebbbe pensare a un attuatore "tenda" per 
        # sopprimere la luce eccessiva
        # per ora il sensore non comunicherà nulla su cui agire

    # def actuator_on(self) -> bool:# ===> tenda 
