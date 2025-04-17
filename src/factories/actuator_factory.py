from actuators.actuator_base import Actuator

ACTUATOR_REGISTRY = {}

def register_actuator(actuator_name): 
    def decorator(cls): 
        ACTUATOR_REGISTRY[actuator_name] = cls
        return cls
    return decorator

def actuator_factory(actuator_type: str, id: str) -> Actuator: 
    actuator_class = ACTUATOR_REGISTRY.get(actuator_type)
    if not actuator_class: 
        raise ValueError(f"Unknown actuator type: {actuator_type}")
    return Actuator(id, actuator_class())
