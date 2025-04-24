from stategraph.state.state import State

def on_light_data(state: State) -> State:
    payload = state.pop("payload", None)

    if payload is None or not isinstance(payload, float): 
        state["events"].append("invalid_payload_light")
        return state 
        # fallback -> stato precedente

    state["light"] += payload 
    state["light_delta"] = payload
    print(f"\n[on_light_data] Updated light to {state['light']}\n")
    return state
