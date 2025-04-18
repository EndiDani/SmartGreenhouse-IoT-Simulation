from common_interfaces        import SensorType
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("air_quality")
class AirQualitySensor(SensorType): 
    def __init__(self): 
        self.state = uniform(.400, 1500.) # ppm - parti per milione

    def receive_data(self, received_data: float):
        k           = 0.005
        delta_co2   = k * (received_data - self.state)
        self.state += delta_co2
        # Per ora intendo il sensore di qualita dell'aria solo come un sensore passivo
        # Formula di simulazione: 
        # ΔCO₂ = k × (C_out – C_in)
        # k: piccolo coefficiente (fa sì che il sistema tenda lentamente al valore esterno (C_out ≈ 400 ppm))

    def check_state(self) -> bool: 
        if self.state> 1500.: 
            return True
        return False
    
    def actuator_on(self, actuator_on: bool) -> bool: 
        if actuator_on: 
            k_fan         = 0.02
            delta_co2_fan = -k_fan * self.state
            self.state   -= delta_co2_fan
            # formula per ridurre il co2
            # identifichiamo un coefficiente di efficacia per il ventilare con k_fan
            if self.state < 1000: 
                actuator_on = not actuator_on
        return actuator_on

    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "air_quality"
