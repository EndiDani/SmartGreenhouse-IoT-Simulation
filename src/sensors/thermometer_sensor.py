from common_interfaces        import SensorType
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("thermometer")
class ThermometerSensor(SensorType): 
    def __init__(self): 
        self.state = uniform(10, 40.)
        self.k     = 0.5
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5
        # ci servirà per calcolare dopo il cambiamento di temperatura in base all'aumento della luce
    # TODO: rendere il valore k assegnabile nell'init

    def receive_data(self, received_data: float):
        self.delta_temp = received_data / 10 * self.k
        self.state     += self.delta_temp 
        # Calcolo l'aumento di temp con questa formula: 
        # - temp_nuova = temp_corrente + Δtemp
        # -- Δtemp = ( ΔLuminosità / 10 ) * k 
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5

    def check_state(self) -> float: 
        if 10. < self.state < 35.: 
            return False
        return True
        # Controllo se il valore è sotto controllo
    # TODO: mettere il min e max nell'init da renderlo customizzabile

    def actuator_on(self, actuator_on: bool) -> bool: 
        if actuator_on:  
            k_fan            = 0.01
            self.delta_temp *= (-k_fan)
            self.state      -= self.delta_temp
            # k_fan: coefficiente efficacia ventilatore per la temperatura            
            if self.state < 30.:
                actuator_on = not actuator_on
        return actuator_on
        
    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "thermometer"
