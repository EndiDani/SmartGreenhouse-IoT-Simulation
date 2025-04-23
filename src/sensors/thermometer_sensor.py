from common_interfaces        import ReactiveSensor
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("thermometer")
class ThermometerSensor(ReactiveSensor): 
    def __init__(
            self, 
            min_temp: float      = 10., 
            max_temp: float      = 35.,
            k: float             = 0.5,
            k_fan: float         = 0.01, 
            act_threshold: float = 30.
            ): 
        self.state         = uniform(min_temp, max_temp)
        self.k             = k
        self.min_temp      = min_temp
        self.max_temp      = max_temp
        self.k_fan         = k_fan
        self.act_threshold = act_threshold

    # Δtemp = ( ΔLuminosità / 10 ) * k 
    def receive_data(self, received_data: float):
        self.delta  = received_data / 10 * self.k
        self.state += self.delta

    def check_state(self) -> float: 
        return not (self.min_temp < self.state < self.max_temp)

    def actuator_on(self) -> bool: 
        self.state -= self.delta * self.k_fan
        return self.state > self.act_threshold
        
    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "thermometer"

    def to_dict(self) -> dict:
        return {    
            "state": self.state,
            "k": self.k,
            "min_temp": self.min_temp,
            "max_temp": self.max_temp,
            "k_fan": self.k_fan,
            "act_threshold": self.act_threshold,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "ThermometerSensor":
        sensor = ThermometerSensor(
            min_temp      = data["min_temp"],
            max_temp      = data["max_temp"],
            k             = data["k"],
            k_fan         = data["k_fan"],
            act_threshold = data["act_threshold"],
        )
        sensor.state = data["state"] 
        return sensor