from sensors.sensor import Sensor
from typing         import Dict, Type

SENSOR_REGISTRY: Dict[str, Type[Sensor]] = {}

def register_sensor(sensor_name): 
    def decorator(cls): 
        SENSOR_REGISTRY[sensor_name] = cls
        return cls
    return decorator

def sensor_factory(sensor_type: str, *args, **kwargs) -> Sensor: 
    sensor_class = SENSOR_REGISTRY.get(sensor_type)   
    if not sensor_class: 
        raise ValueError(f"Unknown sensor type: {sensor_type}")
    instance = sensor_class(*args, **kwargs)
    return Sensor(instance)
