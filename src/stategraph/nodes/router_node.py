from stategraph.state.state import State 

# Mi serve un nodo fittizio per poter instradare correttamente il nodo verso i successivi
def router_checkpoint(state: State) -> dict: 
    return {}

def router_route(state: State):
    # tolgo 'type' dallo state
    type = state.pop("type", None) 
    match type:
        case "light":
            print("[Router] Routing to: on_light_data")
            return "on_light_data"
        case "air_quality":
            print("[Router] Routing to: on_air_quality_data")
            return "on_air_quality_data"
        case _:
            print("[Router] Unknown type, exiting...")
            state["events"].append(f"Unexpected mqtt topic message: {type}")
            return "log_error_node"