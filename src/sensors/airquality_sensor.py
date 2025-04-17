from common_interfaces        import SensorType
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("air_quality")
class AirQualitySensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(.400, 1500.)) # ppm - parti per milione

    def receive_data(self, received_data: float):
        # Per ora intendo il sensore di qualita dell'aria solo come un sensore passivo
        # Formula di simulazione: 
        # ΔCO₂ = k × (C_out – C_in)
        # k: piccolo coefficiente (fa sì che il sistema tenda lentamente al valore esterno (C_out ≈ 400 ppm))
        k = 0.005
        delta_co2 = k * (received_data - self.values[-1])
        self.values.append(self.values[-1] + delta_co2)

    def check_state(self) -> bool: 
        if self.values[-1] > 1500.: 
            self.values.append(self.values[-1]) # appendo il valore che andro a ridurre con la pompa
            return True
        return False

    def get_state(self) -> float: 
        return self.values[-1]
    
    def actuator_on(self, actuator_on: bool) -> bool: 
        if actuator_on: 
            # identifichiamo un coefficiente di efficacia per il ventilare con k_fan
            k_fan = 0.02
            # formula per ridurre il co2
            delta_co2_fan    = -k_fan * self.values[-1]
            self.values[-1] -= delta_co2_fan

            if self.values[-1] < 1000: 
                actuator_on = not actuator_on
        return actuator_on
