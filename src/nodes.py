from random import uniform, randint
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod

# Global sensors register
SENSOR_REGISTRY = {}
def register_sensor(sensor_name): 
    def decorator(cls): 
        SENSOR_REGISTRY[sensor_name] = cls
        return cls
    return decorator

#Global actuator register
ACTUATOR_REGISTRY = {}
def register_actuator(actuator_name): 
    def decorator(cls): 
        ACTUATOR_REGISTRY[actuator_name] = cls
        return cls
    return decorator


class SensorType(ABC): 
    @abstractmethod
    def __init__(self): 
        pass 

    @abstractmethod
    def generate(self): 
        pass
    
    @abstractmethod
    def receive_data(self, received_data: float): 
        pass

    @abstractmethod
    def get_state(self): 
        pass


class ActuatorType(ABC): 
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def switch(self): 
        pass

    @abstractmethod
    def get_state(self):
        pass
    

@register_sensor("thermometer")
class ThermometerSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(-10, 40.))
        self.k = 0.5
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5
        # ci servirà per calcolare dopo il cambiamento di temperatura in base all'aumento della luce

    def generate(self): 
        if randint(1, 2): 
            # se pari il valore sale
            self.values.append(uniform(self.values[-1], self.values[-1] + 4.))
        else: 
            # se dispari scende
            self.values.append(uniform(self.values[-1] - 4., self.values[-1]))

    def receive_data(self, received_data):
        # Nel caso del termometro -> ho ricevuto un aumento o una diminuzione di luce
        # TODO: capire se gestire l'aumento con un valore positivo/negativo o con il valore normale
        # per ora lo gestisco con valore positivo/negativo: evito di memorizzare un valore precedente di luminosita
        # Calcolo l'aumento di temp con questa formula: 
        # - temp_nuova = temp_corrente + Δtemp
        # -- Δtemp = ( ΔLuminosità / 10 ) * k 
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5
        delta_temp = received_data / 10 * self.k
        self.values.append(self.values[-1] + delta_temp)         

    def get_state(self) -> float: 
        return self.values[-1]


@register_sensor("humidity")
class HumiditySensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(10., 90.))

    def generate(self): 
        if randint(1, 2): 
            self.values.append(uniform(self.values[-1], self.values[-1] + 4.))
        else: 
            self.values.append(uniform(self.values[-1] - 4., self.values[-1]))
    
    def receive_data(self, received_data): 
        # la temperatura è aumentata, maggiore evaporazione -> umidità scende piu rapidamente
        # formula molto approsimativa
        # perdita_umidita = 0.1 * temperatura - 1.5
        # per ogni grado in più perdo 0.1% di umidità per ciclo
        # 1.5 è un offset per non avere evaporazione a temperature basse (t <= 15 ad esempio nn ha evaporazioni)
        # es: t: 25 -> 0.1 * 25 * -1.5 = 1.0 --> ho perso 1% di umidità
        loss_humidity = 0.1 * received_data - 1.5
        self.values.append(self.values[-1] - loss_humidity)

    def get_state(self) -> float: 
        return self.values[-1]


@register_sensor("air_quality")
class AirQualitySensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(.10, 149.))

    def generate(self): 
        if randint(1, 2): 
            self.values.append(uniform(self.values[-1], self.values[-1] + 4.))
        else: 
            self.values.append(uniform(self.values[-1] - 4., self.values[-1]))

    def get_state(self) -> float: 
        return self.values[-1]
    
@register_sensor("energy_consume")
class EnergyConsumeSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(10., 500.))
    
    def generate(self): 
        if randint(1, 2): 
            self.values.append(uniform(self.values[-1], self.values[-1] + 4.))
        else: 
            self.values.append(uniform(self.values[-1] - 4., self.values[-1]))   

    def get_state(self) -> float: 
        return self.values[-1]


@register_sensor("light")
class LightSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(0., 4094.))
    
    def generate(self): 
        if randint(1, 2): 
            self.values.append(uniform(self.values[-1], self.values[-1] + 4.))
        else: 
            self.values.append(uniform(self.values[-1] - 4., self.values[-1]))   

    def get_state(self) -> float: 
        return self.values[-1]


@register_actuator("pump")
class PumpSensor(ActuatorType): 
    def __init__(self):
        self.values = []
        self.values.append(False)
    
    def switch(self): 
        self.values.append(not self.values[-1])

    def get_state(self) -> bool: 
        return self.values[-1]
    

@register_actuator("vent")
class VentSensor(ActuatorType): 
    def __init__(self):
        self.values = []
        self.values.append(False)
    
    def switch(self): 
        self.values.append(not self.values[-1])

    def get_state(self) -> bool: 
        return self.values[-1]
      

class Sensor: 
    def __init__(self, id: str, sensor_type: SensorType): 
        self.id = id
        self.sensor_type = sensor_type
        self.state = self.sensor_type.get_state()

    def receive_data(self, recevided_data: float): 
        # Il sensore iscritto al topic riceve il dato che lo influenzerà
        # Chiamo il sensore in particolare per gestire che cosa fare
        # appena gestito aggiorno lo stato anche a questo layer di sensore
        self.sensor_type.receive_data(received_data=recevided_data)
        self.state = self.sensor_type.get_state()
        # TODO: fare logica (e/o controllo che se un valore cambia notifica il sensore)

    def update_state(self): 
        self.state = self.sensor_type.generate()

    def get_id(self) -> str: 
        return self.id

    def get_state(self): 
        self.state = self.sensor_type.get_state()
        return self.state
    
    def __str__(self) -> str: 
        return f"Sensor {self.id} - State: {self.state}" 
    

class Actuator: 
    def __init__(self, id:str, actuator_type: ActuatorType): 
        pass

    # Metodi che attivano gli attuatori, tipo se l'umidità segna < 30% attivo pompa_acqua
    # Metodi che influenzano i sensori, se la pompa è attiva + 10% umidità


def actuator_factory(actuator_type: str, id: str) -> Actuator: 
    actuator_class = ACTUATOR_REGISTRY.get(actuator_type)
    if not actuator_class: 
        raise ValueError(f"Unknow actuator type: {actuator_type}")
    return Actuator(id, actuator_class())


def sensor_factory(sensor_type: str, id: str) -> Sensor: 
    sensor_class = SENSOR_REGISTRY.get(sensor_type)   
    if not sensor_class: 
        raise ValueError(f"Unknown sensor type: {sensor_type}")
    return Sensor(id, sensor_class())









class Node(): 
    def __init__(self, sensor: Sensor): 
        pass


class Broker(): 
    def __init__(self): 
        self.topic_data: Dict[str, List] = {}
        self.topic_subscribed: Dict[str, List] = {}

    def receive_data(self, received: Tuple[str, str, float]): 
        id    = received[0]
        topic = received[1]
        data  = received[2]

        if topic not in self.topic_subscribed: 
            print("The device is not registered in any topic.")
            return 
        
        self.topic_data[topic].append(data)
        self.publish(topic, id)

    def publish(self, topic: str, id: str): 
        sensors = [
            sensor
            for sensor in self.topic_subscribed[topic] 
            if sensor.get_id() != id
        ]

        if sensors: 
            for sensor in sensors: 
                sensor.receive_data(self.topic_data[topic][-1])
                
    def subscribe(self, topic: str, node: Node): 
        if topic not in self.topic_subscribed: 
            self.topic_subscribed[topic] = []
            self.topic_data[topic] = []

        self.topic_subscribed[topic].append(node)
        self.topic_data[topic].append(node.get_state())


