from stategraph.state.state import State 

def router_route(state: State):
    match state["type"]:
        case "light":
            return "on_light_data"
        case "air_quality":
            return "on_air_quality_data"
        case _:
            print(f"[ERROR] Unexpected mqtt topic message: {state['type']}")
            return "log_error_node"