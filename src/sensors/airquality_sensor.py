from common_interfaces        import ReactiveSensor
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("air_quality")
class AirQualitySensor(ReactiveSensor): 
    def __init__(
            self, 
            min_ppm: float       = 400.,
            max_ppm: float       = 1500., 
            k: float             = 0.05, 
            k_fan: float         = 0.02,
            act_threshold: float = 1000.
            ): 
        self.state         = uniform(min_ppm, max_ppm)
        self.min_ppm       = min_ppm
        self.max_ppm       = max_ppm
        self.k             = k
        self.k_fan         = k_fan
        self.act_threshold = act_threshold

    # ΔCO₂ = k × (C_out – C_in)
    def receive_data(self, received_data: float):
        delta_co2   = self.k * (received_data - self.state)
        self.state += delta_co2
        self.state  = max(self.min_ppm, min(self.state, self.max_ppm + 500))

    def check_state(self) -> bool: 
        return self.state > self.max_ppm
  
    def actuator_on(self) -> bool: 
        delta_co2_fan = -self.k_fan * self.state
        self.state   -= delta_co2_fan
        return self.state < self.act_threshold

    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "air_quality"

    def to_dict(self) -> dict:
        return {
            "class": self.__class__.__name__,  # "AirQualitySensor"
            "state": self.state,
            "min_ppm": self.min_ppm,
            "max_ppm": self.max_ppm,
            "k": self.k,
            "k_fan": self.k_fan,
            "act_threshold": self.act_threshold,
        }

    @staticmethod
    def from_dict(data: dict) -> "AirQualitySensor":
        sensor = AirQualitySensor(
            min_ppm       = data["min_ppm"],
            max_ppm       = data["max_ppm"],
            k             = data["k"],
            k_fan         = data["k_fan"],
            act_threshold = data["act_threshold"],
        )
        sensor.state = data["state"]
        return sensor
