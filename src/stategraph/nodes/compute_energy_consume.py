from stategraph.state.state import State 

def compute_energy_consume(state: State) -> State: 
    try: 
        energy_consume = state["env"]["idle_power"]
        if state["vent_on"]: 
            energy_consume += state["env"]["power_rating_vent"]
        if state["pump_on"]: 
            energy_consume += state["env"]["power_rating_pump"]
    except Exception as e: 
        state["events"].append(f"computation error in energy_consume: {str(e)}")

    state["energy_consume"] = energy_consume
    print(f"[compute_energy_consume] Energy consumed: {state['energy_consume']}\n\n")
    return state