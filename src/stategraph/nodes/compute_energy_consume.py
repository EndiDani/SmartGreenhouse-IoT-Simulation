from stategraph.state.state import State 

def compute_energy_consume(state: State) -> State: 
    events_to_add = []
    steps_to_add  = []
    try: 
        energy_consume = state["env"]["idle_power"]
        if state["vent_on"]: 
            energy_consume += state["env"]["power_rating_vent"]
        if state["pump_on"]: 
            energy_consume += state["env"]["power_rating_pump"]
    except Exception as e: 
        events_to_add.append(f"computation error in energy_consume: {str(e)}")

    state["energy_consume"] = energy_consume
    steps_to_add.append(f"[compute_energy_consume] Energy consumed: {state['energy_consume']}")
    
    return {
        "energy_consume": state["energy_consume"], 
        "steps": steps_to_add,
        "events": events_to_add
    }