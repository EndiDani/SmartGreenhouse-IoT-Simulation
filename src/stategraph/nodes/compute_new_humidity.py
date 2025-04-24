from stategraph.state.state import State 

# Δumidità = evap_coeff * temp - evap_offset 
def compute_new_humidity(state: State) -> State:
    try: 
        rate = state["env"]["evap_coeff"] * state["thermometer"] - state["env"]["evap_offset"]
        state["evaporation_rate"] = max(rate, 0.0)
        state["humidity"] -= state["evaporation_rate"]
    except Exception as e: 
        state["events"].append(f"computation error in humidity: {str(e)}")
          
    print(f"[compute_new_humidity] Updated humidity to {state['humidity']}\n")
    return state