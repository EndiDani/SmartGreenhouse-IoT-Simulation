from stategraph.state.state import State 

def on_air_quality_data(state: State) -> State:
    steps_to_add  = []
    events_to_add = []
    payload = state["payload"]

    steps_to_add.append("[Routed] Routing to: on_air_quality_data")

    if payload is None or not isinstance(payload, float) or payload < 400.: 
        events_to_add.append("invalid_payload_air_quality")
        return {"events": events_to_add}

    state["air_quality"] = payload
    steps_to_add.append(f"[on_air_quality_data] Updated air_quality to {state['air_quality']}")

    return {
        "air_quality": state["air_quality"],
        "steps": steps_to_add,
    }