from common_interfaces import BasicSensor, ReactiveSensor


class Sensor: 
    def __init__(self, id: str, sensor_type: BasicSensor): 
        self.id          = id
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
            self.sensor_type.check_state()
        )

    def get_id(self) -> str: 
        return self.id

    def get_state(self): 
        return self.sensor_type.get_state()
    
    def get_sensortype(self) -> str:
        return self.sensor_type.get_type()
    
    def __str__(self) -> str: 
        return f"Sensor {self.id} - State: {self.state}" 
