from common_interfaces        import SensorType
from random                   import uniform
from factories.sensor_factory import register_sensor

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



    