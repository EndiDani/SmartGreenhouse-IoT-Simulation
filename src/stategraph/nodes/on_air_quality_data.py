from stategraph.state.state import State 

def on_air_quality_data(state: State) -> State:
    payload = state["payload"]

    if payload is None or not isinstance(payload, float) or payload < 400.: 
        state["events"].append("invalid_payload_air_quality")
        return {"events": state["events"]}

    state["air_quality"] = payload
    print(f"\n[on_air_quality_data] Updated air_quality to {state['air_quality']}\n")
    return {"air_quality": state["air_quality"]}