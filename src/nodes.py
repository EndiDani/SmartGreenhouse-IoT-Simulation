from random import uniform, randint
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
from datetime import datetime

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
    def receive_data(self, received_data: float): 
        pass

    @abstractmethod
    def check_state(self) -> bool: 
        pass

    @abstractmethod
    def get_state(self) -> float: 
        pass

    @abstractmethod
    def actuator_on(self, actuator_on: bool) -> bool: 
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
    def get_time(self) -> float: 
        pass

    @abstractmethod
    def get_consume(self) -> float:
        pass

    @abstractmethod
    def is_on(self) -> bool: 
        pass
   

@register_sensor("thermometer")
class ThermometerSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(-10, 40.))
        self.k = 0.5
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5
        # ci servirà per calcolare dopo il cambiamento di temperatura in base all'aumento della luce
        # TODO: rendere il valore k assegnabile nell'init

    def receive_data(self, received_data: float):
        # Calcolo l'aumento di temp con questa formula: 
        # - temp_nuova = temp_corrente + Δtemp
        # -- Δtemp = ( ΔLuminosità / 10 ) * k 
        # coefficiente k: coefficiente assorbimento termico, ipotezziamo per ora a 0.5
        self.delta_temp = received_data / 10 * self.k
        self.values.append(self.values[-1] + self.delta_temp)      

    def check_state(self) -> float: 
        # Controllo se il valore è sotto controllo
        # TODO: mettere il min e max nell'init da renderlo customizzabile
        if 10. < self.values[-1] < 35.: 
            self.values.append(self.values[-1]) # appendo il valore che andro a ridurre con la pompa
            return False
        return True
        
    def get_state(self) -> float: 
        return self.values[-1]

    def actuator_on(self, actuator_on: bool): 
        if actuator_on: 
            # Coefficiente efficacia ventilatore per la temperatura
            k_fan = 0.01
            self.delta_temp *= (-k_fan)
            self.values[-1] -= self.delta_temp

            if self.values[-1] < 30:
                actuator_on = not actuator_on
        return actuator_on


@register_sensor("humidity")
class HumiditySensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(10., 90.))
        self.lastTemperature = 0.

    def receive_data(self, received_data: float): 
        # la temperatura è aumentata, maggiore evaporazione -> umidità scende piu rapidamente
        # formula molto approsimativa
        # perdita_umidita = 0.1 * temperatura - 1.5
        # per ogni grado in più perdo 0.1% di umidità per ciclo
        # 1.5 è un offset per non avere evaporazione a temperature basse (t <= 15 ad esempio nn ha evaporazioni)
        # es: t: 25 -> 0.1 * 25 * -1.5 = 1.0 --> ho perso 1% di umidità
        self.lastTemperature = received_data
        self.evaporation_rate = 0.1 * self.lastTemperature - 1.5
        self.values.append(self.values[-1] - self.evaporation_rate)

    def check_state(self) -> bool:
        # TODO: customizzare la percentuale di umidita minima
        if self.values[-1] < 30.:  
            self.values.append(self.values[-1]) # appendo il valore che andro a ridurre con la pompa
            return True
        return False

    def get_state(self) -> float: 
        return self.values[-1]
    
    def actuator_on(self, actuator_on: bool) -> bool: 
        if actuator_on: 
            # Invertiamo la formula per innalzare l'umidità
            pump_gain = 5.
            net_gain = pump_gain - self.evaporation_rate
            # self.values.append(self.values[-1] + net_gain) -> per ora aggiorno direttamente l'ultimo valore
            self.values[-1] += net_gain
            
            if self.values[-1] > 60: 
                actuator_on = not actuator_on # sopra il 60% avviso di spegnere la pompa
        return actuator_on


@register_sensor("air_quality")
class AirQualitySensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(.400, 1500.)) # ppm - parti per milione

    def receive_data(self, received_data: float):
        # Per ora intendo il sensore di qualita dell'aria solo come un sensore passivo
        # Formula di simulazione: 
        # ΔCO₂ = k × (C_out – C_in)
        # k: piccolo coefficiente (fa sì che il sistema tenda lentamente al valore esterno (C_out ≈ 400 ppm))
        k = 0.005
        delta_co2 = k * (received_data - self.values[-1])
        self.values.append(self.values[-1] + delta_co2)

    def check_state(self) -> bool: 
        if self.values[-1] > 1500.: 
            self.values.append(self.values[-1]) # appendo il valore che andro a ridurre con la pompa
            return True
        return False

    def get_state(self) -> float: 
        return self.values[-1]
    
    def actuator_on(self, actuator_on: bool) -> bool: 
        if actuator_on: 
            # identifichiamo un coefficiente di efficacia per il ventilare con k_fan
            k_fan = 0.02
            # formula per ridurre il co2
            delta_co2_fan = -k_fan * self.values[-1]
            self.values[-1] -= delta_co2_fan

            if self.values[-1] < 1000: 
                actuator_on = not actuator_on
        return actuator_on

    
@register_sensor("energy_consume")
class EnergyConsumeSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.idle_power = 6.3 # Watt
        self.values.append(self.idle_power)
    
    def receive_data(self, received_data: float):
        # I dati ricevuti saranno il consumo energetico degli attuatori
        self.values.append(self.idle_power + received_data)

    def check_state(self) -> bool:
        # self.values.append(self.values[-1])
        return False

    def get_state(self) -> float: 
        return self.values[-1]
    
    def actuator_on(self, actuator_on: bool) -> bool: 
        if actuator_on: 
            pass # applicare logica in futuro


@register_sensor("light")
class LightSensor(SensorType): 
    def __init__(self): 
        self.values = []
        self.values.append(uniform(0., 4094.))

    def receive_data(self, received_data: float):
        # Questo puo essere inteso come un aumento di luce da fonti esterne al sensore
        # quindi un aumento non dipendente da altri sensori
        self.values.append(self.values[-1] + received_data)

    def check_state(self) -> bool:
        # TODO: In futuro si potrebbbe pensare a un attuatore "tenda" per 
        # sopprimere la luce eccessiva
        # per ora il sensore non comunicherà nulla su cui agire
        return False       

    def get_state(self) -> float: 
        return self.values[-1]
    
    # def actuator_on(self, actuator_on: bool) -> bool: ===> tenda 


@register_actuator("pump")
class PumpActuator(ActuatorType): 
    def __init__(self):
        self.time_spent = [0.]
        self.powered = False
        self.power_rating = 12. # Wh 
    
    def switch(self): 
        self.powered = not self.powered
        self.time_on()
    
    def time_on(self): 
        if self.powered: 
            self.activation_start_time = datetime.now()
        else: 
            duration = datetime.now() - self.activation_start_time
            self.time_spent.append(duration.total_seconds())

    def get_time(self) -> float: 
        if self.powered:
            return datetime.now() - self.activation_start_time
        return float(self.time_spent[-1])
    
    def get_consume(self) -> float: 
        hours = self.get_time() / 3600
        return self.power_rating * hours
    
    def is_on(self) -> bool: 
        return self.powered
    

@register_actuator("vent")
class VentActuator(ActuatorType): 
    def __init__(self):
        self.time_spent = [0.]
        self.powered = False
        self.power_rating = 8. # Wh 
    
    def switch(self): 
        self.powered = not self.powered
        self.time_on()
    
    def time_on(self): 
        if self.powered: 
            self.activation_start_time = datetime.now()
        else: 
            duration = datetime.now() - self.activation_start_time
            self.time_spent.append(duration.total_seconds())

    def get_time(self) -> float: 
        if self.powered:
            return datetime.now() - self.activation_start_time
        return float(self.time_spent[-1])
    
    def get_consume(self) -> float: 
        hours = self.get_time() / 3600
        return self.power_rating * hours
    
    def is_on(self) -> bool: 
        return self.powered
      

class Sensor: 
    def __init__(self, id: str, sensor_type: SensorType): 
        self.id = id
        self.sensor_type = sensor_type
        self.state = self.sensor_type.get_state()

    def receive_data(self, received_data: float): 
        # Il sensore iscritto al topic riceve il dato che lo influenzerà
        # Chiamo il sensore in particolare per gestire che cosa fare
        # appena gestito aggiorno lo stato anche a questo layer di sensore
        self.sensor_type.receive_data(received_data)
        self.state = self.sensor_type.get_state()
        # TODO: fare logica (e/o controllo che se un valore cambia notifica il sensore)

    # def update_state(self): 
    #    self.state = self.sensor_type.generate()

    def get_id(self) -> str: 
        return self.id

    def get_state(self): 
        self.state = self.sensor_type.get_state()
        return self.state
    
    def __str__(self) -> str: 
        return f"Sensor {self.id} - State: {self.state}" 
    

class Actuator: 
    def __init__(self, id: str, actuator_type: ActuatorType): 
        self.id = id
        self.actuator_type = actuator_type
    
    def switch(self): 
        self.actuator_type.switch()
    
    def get_time(self) -> float: 
        return self.actuator_type.get_time()
    
    def power_consumption(self) -> float:
        return self.actuator_type.get_consume()
    
    


    # Metodi che attivano gli attuatori, tipo se l'umidità segna < 30% attivo pompa_acqua
    # Metodi che influenzano i sensori, se la pompa è attiva + 10% umidità


def actuator_factory(actuator_type: str, id: str) -> Actuator: 
    actuator_class = ACTUATOR_REGISTRY.get(actuator_type)
    if not actuator_class: 
        raise ValueError(f"Unknown actuator type: {actuator_type}")
    return Actuator(id, actuator_class())


def sensor_factory(sensor_type: str, id: str) -> Sensor: 
    sensor_class = SENSOR_REGISTRY.get(sensor_type)   
    if not sensor_class: 
        raise ValueError(f"Unknown sensor type: {sensor_type}")
    return Sensor(id, sensor_class())







'''

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

'''
