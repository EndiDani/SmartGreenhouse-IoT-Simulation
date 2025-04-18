from common_interfaces import ActuatorType  


class Actuator: 
    def __init__(self, id: str, actuator_type: ActuatorType): 
        self.id = id
        self.actuator_type = actuator_type
    
    def switch(self): 
        self.actuator_type.switch()
    
    def get_time(self) -> float: 
        return self.actuator_type.get_time()
    
    def get_consume(self) -> float:
        return self.actuator_type.get_consume()
    
    def is_on(self) -> bool: 
        return self.actuator_type.is_on()
    
    def get_actuatortype(self) -> str:
        return self.actuator_type.get_actuatortype()
