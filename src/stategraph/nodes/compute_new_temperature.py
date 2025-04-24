from stategraph.state.state import State 

# Δtemp = ( ΔLuminosità / 10 ) * k 
def compute_new_temperature(state: State) -> State: 
    try: 
        delta = state["light_delta"] / 10 * state["env"]["k_temp"]
        state["delta_temp"] = delta
        state["thermometer"] += state["delta_temp"]
    except Exception as e: 
        state["events"].append(f"computation error in temperature: {str(e)}")

    print(f"[compute_new_temperature] Updated thermometer to {state['thermometer']}\n")
    return state
