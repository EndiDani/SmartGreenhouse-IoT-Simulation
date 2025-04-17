from common_interfaces import ActuatorType  

class Actuator: 
    def __init__(self, id: str, actuator_type: ActuatorType): 
        self.id = id
        self.actuator_type = actuator_type
    
    def switch(self): 
        self.actuator_type.switch()
    
    def get_time(self) -> float: 
        return self.actuator_type.get_time()
    
    def power_consumption(self) -> float:
        return self.actuator_type.get_consume()
      