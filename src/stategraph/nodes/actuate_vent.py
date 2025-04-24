from stategraph.state.state import State 

def actuate_vent(state: State) -> State: 
    # Termometro:
    try: 
        delta_actuator = state["delta_temp"] * state["env"]["k_fan_temp"]
        state["thermometer"] -= delta_actuator
    except Exception as e: 
        state["events"].append(f"computation error in actuate_vent (thermometer): {str(e)}")

    check_temp = state["thermometer"] < state["env"]["act_threshold_temp"]
    
    # Qualita aria:
    try:  
        delta_actuator = -state["env"]["k_fan_air"] * state["air_quality"]
        state["air_quality"] -= delta_actuator
    except Exception as e: 
        state["events"].append(f"computation error in actuate_vent (air_quality): {str(e)}")

    check_air_quality = state["air_quality"] > state["act_threshold_air"]

    # Controllo ventola
    state["vent_on"] = check_temp or check_air_quality
    print(f"[actuate_vent] Actuation completed:\nVent: {state['vent_on']}\nTemp: {state['thermometer']}\nAir quality: {state['air_quality']}\n")
    return state
