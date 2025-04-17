from sensors.sensor_base import Sensor

SENSOR_REGISTRY = {}

def register_sensor(sensor_name): 
    def decorator(cls): 
        SENSOR_REGISTRY[sensor_name] = cls
        return cls
    return decorator

def sensor_factory(sensor_type: str, id: str) -> Sensor: 
    sensor_class = SENSOR_REGISTRY.get(sensor_type)   
    if not sensor_class: 
        raise ValueError(f"Unknown sensor type: {sensor_type}")
    return Sensor(id, sensor_class())
