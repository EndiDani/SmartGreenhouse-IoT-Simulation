from stategraph.state.state import State 

# Δumidità = evap_coeff * temp - evap_offset 
def compute_new_humidity(state: State) -> State:
    events_to_add = []
    steps_to_add  = []
    try: 
        rate = state["env"]["evap_coeff"] * state["thermometer"] - state["env"]["evap_offset"]
        state["evaporation_rate"] = max(rate, 0.0)
        state["humidity"] -= state["evaporation_rate"]
    except Exception as e: 
        events_to_add.append(f"computation error in humidity: {str(e)}")
          
    steps_to_add.append(f"[compute_new_humidity] Updated humidity to {state['humidity']}")
    
    return {
        "humidity": state["humidity"], 
        "evaporation_rate": state["evaporation_rate"], 
        "steps": steps_to_add,
        "events": events_to_add
    }