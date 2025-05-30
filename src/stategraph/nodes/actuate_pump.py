from stategraph.state.state import State 

def actuate_pump(state: State) -> State: 
    events_to_add = []
    steps_to_add  = []
    try: 
        net_gain = state["env"]["pump_gain"] - state["evaporation_rate"]
        state["humidity"] += net_gain
    except Exception as e: 
        events_to_add.append(f"computation error in actuate_pump: {str(e)}")

    state["pump_on"] = state["humidity"] < state["env"]["act_threshold_humidity"]
    steps_to_add.append(f"[actuate_pump] Actuation completed:\nPump: {state['pump_on']}\nHumidity: {state['humidity']}")

    return {
        "humidity": state["humidity"], 
        "pump_on": state["pump_on"], 
        "steps": steps_to_add,
        "events": events_to_add
    }
