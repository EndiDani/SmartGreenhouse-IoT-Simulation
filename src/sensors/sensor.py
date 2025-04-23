from common_interfaces import BasicSensor, ReactiveSensor


class Sensor: 
    def __init__(self, sensor_type: BasicSensor): 
        self.sensor_type = sensor_type

    def receive_data(self, received_data: float): 
        self.sensor_type.receive_data(received_data)
    
    def check_state(self) -> bool: 
        return (
            isinstance(self.sensor_type, ReactiveSensor) 
            and 
            self.sensor_type.check_state()
        )
    
    def actuator_on(self) -> bool: 
        return (
            isinstance(self.sensor_type, ReactiveSensor) 
            and 
            self.sensor_type.actuator_on()
        )
    
    def get_state(self): 
        return self.sensor_type.get_state()
    
    def get_sensortype(self) -> str:
        return self.sensor_type.get_sensortype()
    
    def __str__(self) -> str: 
        return f"Sensor {self.id} - State: {self.state}" 
    
    def to_dict(self):
        return self.sensor_type.to_dict()

    @staticmethod
    def from_dict(data: dict) -> "Sensor":
        from factories.sensor_factory import SENSOR_REGISTRY 

        sensor_class = SENSOR_REGISTRY.get(data["sensor_type"])
        sensor_type = sensor_class.from_dict(data["state"])
        return Sensor(sensor_type)