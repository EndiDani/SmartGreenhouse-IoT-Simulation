from stategraph.state.state import State 

def actuate_pump(state: State) -> State: 
    try: 
        net_gain = state["env"]["pump_gain"] - state["evaporation_rate"]
        state["humidity"] += net_gain
    except Exception as e: 
        state["events"].append(f"computation error in actuate_pump: {str(e)}")

    state["pump_on"] = state["humidity"] < state["env"]["act_threshold_humidity"]
    print(f"[actuate_pump] Actuation completed:\nPump: {state['pump_on']}\nHumidity: {state['humidity']}\n")
    return state
