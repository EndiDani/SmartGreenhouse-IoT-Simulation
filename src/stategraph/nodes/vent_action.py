from stategraph.state.state import State 
from langgraph.types import Command
from typing import Literal

def vent_action(state: State) -> Command[Literal["actuate_vent", "compute_energy_consume"]]: 
    if state["vent_on"]: 
        print(f"[vent_action] Vent is {'on' if state['vent_on'] else 'off'}, routing to: actuate_vent\n")
        return Command(update={}, goto="actuate_vent")
    
    air_quality = state["air_quality"]
    max_air_allowed = state["env"]["max_ppm"]

    temperature = state["thermometer"]
    max_temp_allowed = state["env"]["max_temp"]

    needs_vent_for_air  = air_quality > max_air_allowed
    needs_vent_for_temp = temperature > max_temp_allowed

    state["vent_on"] = needs_vent_for_air or needs_vent_for_temp
    print(f"[vent_action] Check completed, vent is in {'on' if state['vent_on'] else 'off'}\n")
    return Command(update={"vent_on": state["vent_on"]}, goto="compute_energy_consume")