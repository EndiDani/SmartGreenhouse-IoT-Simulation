from common_interfaces        import ReactiveSensor
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("humidity")
class HumiditySensor(ReactiveSensor): 
    def __init__(
            self, 
            min_hum: float      = 30., 
            max_hum: float      = 80.,
            evap_coeff: float   = 0.1, 
            evap_offset: float  = 1.5, 
            pump_gain: float    = 5., 
            act_threshold:float = 60.,
            ): 
        self.state             = uniform(min_hum, max_hum)
        self.min_hum           = min_hum
        self.max_hum           = max_hum
        self.evap_coeff        = evap_coeff
        self.evap_offset       = evap_offset
        self.pump_gain         = pump_gain
        self.act_threshold     = act_threshold

    # Δumidità = evap_coeff * temp - evap_offset 
    def receive_data(self, received_data: float):
        rate = self.evap_coeff * received_data - self.evap_offset
        self.evaporation_rate = max(rate, 0.0)
        self.state -= self.evaporation_rate
 
    def check_state(self) -> bool:
        return self.state < self.min_hum
        
    def actuator_on(self) -> bool: 
        net_gain = self.pump_gain - self.evaporation_rate
        self.state += net_gain
        return self.state > self.act_threshold

    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "humidity"

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "min_hum": self.min_hum,
            "max_hum": self.max_hum,
            "evap_coeff": self.evap_coeff,
            "evap_offset": self.evap_offset,
            "pump_gain": self.pump_gain,
            "act_threshold": self.act_threshold,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "HumiditySensor":
        sensor = HumiditySensor(
            min_hum       = data["min_hum"],
            max_hum       = data["max_hum"],
            evap_coeff    = data["evap_coeff"],
            evap_offset   = data["evap_offset"],
            pump_gain     = data["pump_gain"],
            act_threshold = data["act_threshold"]
        )
        sensor.state = data["state"]
        return sensor