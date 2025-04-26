from stategraph.state.state import State 
from langgraph.types        import Command
from typing                 import Literal

def pump_action(state: State) -> Command[Literal["actuate_pump","compute_energy_consume"]]:
    steps_to_add = []

    if state["pump_on"]:
        steps_to_add.append(f"[pump_action] Pump is {'on' if state['pump_on'] else 'off'}, routing to: actuate_pump\n")
        return Command(update={}, goto="actuate_pump")
    
    humidity = state["humidity"]
    min_allowed = state["env"]["min_hum"]

    need_pump = humidity < min_allowed
    state["pump_on"] = need_pump
    steps_to_add.append(f"[pump_action] Check completed, pump is in {'on' if state['pump_on'] else 'off'}")
    return Command(
        update = {
            "pump_on": state["pump_on"],
            "steps": steps_to_add
        }, 
        goto = "compute_energy_consume"
    )