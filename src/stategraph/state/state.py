from typing   import Annotated, TypedDict, List, Dict
from operator import add

class State(TypedDict): 
    zone:             str
    light:            float
    light_delta:      float
    thermometer:      float
    delta_temp:       float
    air_quality:      float
    humidity:         float
    evaporation_rate: float
    energy_consume:   float
    vent_on:          bool
    pump_on:          bool
    neighbors:        List[str]
    env:              Dict[str, float]
    steps:            Annotated[List[str], add] # traccia del grafo per tenerlo sequenziale anche in async
    events:           Annotated[List[str], add] # lista di eventi critici attivi
    payload:          float
    type:             str
