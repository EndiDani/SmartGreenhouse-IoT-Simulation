from stategraph.state.state import State

def on_light_data(state: State) -> State:
    steps_to_add  = []
    events_to_add = []
    payload = state["payload"]

    steps_to_add.append("[Routed] Routing to: on_light_data")

    if payload is None or not isinstance(payload, float): 
        events_to_add.append("invalid_payload_light")
        return {"events": events_to_add}

    state["light"] += payload 
    state["light_delta"] = payload
    steps_to_add.append(f"[on_light_data] Updated light to {state['light']}")
    return {
        "light": state["light"], 
        "light_delta": state["light_delta"],
        "steps": steps_to_add,
    }
