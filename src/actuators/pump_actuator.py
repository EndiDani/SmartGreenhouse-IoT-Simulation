from common_interfaces          import ActuatorType
from datetime                   import datetime
from factories.actuator_factory import register_actuator


@register_actuator("pump")
class PumpActuator(ActuatorType): 
    def __init__(self):
        self.time_spent   = [0.]
        self.powered      = False
        self.power_rating = 12. # Wh 
    
    def switch(self): 
        self.powered = not self.powered
        self.time_on()
    
    def time_on(self): 
        if self.powered: 
            self.activation_start_time = datetime.now()
        else: 
            duration = datetime.now() - self.activation_start_time
            self.time_spent.append(duration.total_seconds())

    def is_on(self) -> bool: 
        return self.powered

    def get_time(self) -> float: 
        if self.powered:
            return datetime.now() - self.activation_start_time
        return float(self.time_spent[-1])
    
    def get_consume(self) -> float: 
        hours = self.get_time() / 3600
        return self.power_rating * hours

    def get_actuatortype(self) -> str:
        return "pump"
