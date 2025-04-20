from common_interfaces import ActuatorType  


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
