from common_interfaces          import ActuatorType
from factories.actuator_factory import register_actuator


@register_actuator("vent")
class VentActuator(ActuatorType): 
    def __init__(self):
        self.powered      = False
        self.power_rating = 8. # Wh 
    
    def switch(self): 
        self.powered = not self.powered

    def is_on(self) -> bool: 
        return self.powered
    
    def get_consume(self) -> float: 
        return self.power_rating 
    
    def get_actuatortype(self) -> str:
        return "vent"

    def to_dict(self) -> dict: 
        return {
            "powered": self.powered,
            "power_rating": self.power_rating
        }
    
    @staticmethod
    def from_dict(data: dict) -> "VentActuator": 
        actuator              = VentActuator()
        actuator.powered      = data["powered"]
        actuator.power_rating = data["power_rating"]
        return actuator