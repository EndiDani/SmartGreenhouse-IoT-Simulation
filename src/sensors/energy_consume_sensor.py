from common_interfaces        import SensorType
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("energy_consume")
class EnergyConsumeSensor(SensorType): 
    def __init__(self): 
        self.values     = []
        self.idle_power = 6.3 # Watt
        self.values.append(self.idle_power)
    
    def receive_data(self, received_data: float):
        # I dati ricevuti saranno il consumo energetico degli attuatori
        self.values.append(self.idle_power + received_data)

    def check_state(self) -> bool:
        # self.values.append(self.values[-1])
        return False

    def get_state(self) -> float: 
        return self.values[-1]
    
    def actuator_on(self, actuator_on: bool) -> bool: 
        if actuator_on: 
            pass # applicare logica in futuro
