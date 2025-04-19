from common_interfaces        import ReactiveSensor
from random                   import uniform
from factories.sensor_factory import register_sensor


@register_sensor("humidity")
class HumiditySensor(ReactiveSensor): 
    def __init__(self): 
        self.state = uniform(10., 90.)

    def receive_data(self, received_data: float): 
        self.lastTemperature  = received_data
        self.evaporation_rate = 0.1 * self.lastTemperature - 1.5
        self.state           -= self.evaporation_rate
        # la temperatura è aumentata, maggiore evaporazione -> umidità scende piu rapidamente
        # formula molto approsimativa
        # perdita_umidita = 0.1 * temperatura - 1.5
        # per ogni grado in più perdo 0.1% di umidità per ciclo
        # 1.5 è un offset per non avere evaporazione a temperature basse (t <= 15 ad esempio nn ha evaporazioni)
        # es: t: 25 -> 0.1 * 25 * -1.5 = 1.0 --> ho perso 1% di umidità

    # TODO: customizzare la percentuale di umidita minima
    def check_state(self) -> bool:
        if self.state < 30.:  
            return True
        return False
        
    # Invertiamo la formula per innalzare l'umidità
    def actuator_on(self) -> bool: 
        pump_gain   = 5.
        net_gain    = pump_gain - self.evaporation_rate
        self.state += net_gain
        if self.state > 60.: 
            return True
        return False

    def get_state(self) -> float: 
        return self.state
    
    def get_sensortype(self) -> str: 
        return "humidity"
