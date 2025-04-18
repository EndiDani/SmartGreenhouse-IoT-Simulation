from abc import ABC, abstractmethod


class SensorType(ABC): 
    @abstractmethod
    def __init__(self): 
        pass 
    
    @abstractmethod
    def receive_data(self, received_data: float): 
        pass

    @abstractmethod
    def check_state(self) -> bool: 
        pass

    @abstractmethod
    def actuator_on(self, actuator_on: bool) -> bool: 
        pass

    @abstractmethod
    def get_state(self) -> float: 
        pass

    @abstractmethod
    def get_sensortype(self) -> str:
        pass


class ActuatorType(ABC): 
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def switch(self): 
        pass

    @abstractmethod
    def time_on(self): 
        pass

    @abstractmethod
    def is_on(self) -> bool: 
        pass

    @abstractmethod
    def get_time(self) -> float: 
        pass

    @abstractmethod
    def get_consume(self) -> float:
        pass

    @abstractmethod
    def get_actuatortype(self) -> str:
        pass
