from stategraph.state.state import State 

# Δtemp = ( ΔLuminosità / 10 ) * k 
def compute_new_temperature(state: State) -> State: 
    events_to_add = []
    steps_to_add  = []
    try: 
        delta = state["light_delta"] / 10 * state["env"]["k_temp"]
        state["delta_temp"] = delta
        state["thermometer"] += state["delta_temp"]
    except Exception as e: 
        events_to_add.append(f"computation error in temperature: {str(e)}")

    steps_to_add.append(f"[compute_new_temperature] Updated thermometer to {state['thermometer']}")
    
    return {
        "thermometer": state["thermometer"], 
        "delta_temp": state["delta_temp"], 
        "steps": steps_to_add,
        "events": events_to_add
    }
