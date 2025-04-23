from common_interfaces          import ActuatorType  


class Actuator: 
    def __init__(self, actuator_type: ActuatorType): 
        self.actuator_type = actuator_type
    
    def switch(self): 
        self.actuator_type.switch()
    
    def is_on(self) -> bool: 
        return self.actuator_type.is_on()
    
    def get_consume(self) -> float:
        return self.actuator_type.get_consume()
    
    def get_actuatortype(self) -> str:
        return self.actuator_type.get_actuatortype()

    def to_dict(self): 
        return {
            "class": self.actuator_type.__class__.__name__,
            "actuator_type": self.get_actuatortype(),
            "state": self.actuator_type.to_dict()
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Actuator":
        from factories.actuator_factory import ACTUATOR_REGISTRY
        
        actuator_class = ACTUATOR_REGISTRY.get(data["actuator_type"])  
        actuator_type = actuator_class.from_dict(data["state"])  
        return Actuator(actuator_type)  