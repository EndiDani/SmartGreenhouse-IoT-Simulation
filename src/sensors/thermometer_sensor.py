from common_interfaces        import SensorType
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("thermometer")
class ThermometerSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(-10, 40.))
        self.k = 0.5
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5
        # ci servirà per calcolare dopo il cambiamento di temperatura in base all'aumento della luce
        # TODO: rendere il valore k assegnabile nell'init

    def receive_data(self, received_data: float):
        # Calcolo l'aumento di temp con questa formula: 
        # - temp_nuova = temp_corrente + Δtemp
        # -- Δtemp = ( ΔLuminosità / 10 ) * k 
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5
        self.delta_temp = received_data / 10 * self.k
        self.values.append(self.values[-1] + self.delta_temp)      

    def check_state(self) -> float: 
        # Controllo se il valore è sotto controllo
        # TODO: mettere il min e max nell'init da renderlo customizzabile
        if 10. < self.values[-1] < 35.: 
            self.values.append(self.values[-1]) # appendo il valore che andro a ridurre con la pompa
            return False
        return True
        
    def get_state(self) -> float: 
        return self.values[-1]

    def actuator_on(self, actuator_on: bool): 
        if actuator_on: 
            # Coefficiente efficacia ventilatore per la temperatura
            k_fan = 0.01
            self.delta_temp *= (-k_fan)
            self.values[-1] -= self.delta_temp

            if self.values[-1] < 30:
                actuator_on = not actuator_on
        return actuator_on
    