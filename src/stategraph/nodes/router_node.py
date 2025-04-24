from stategraph.state.state import State 

# Mi serve un nodo fittizio per poter instradare correttamente il nodo verso i successivi
def router(state: State) -> dict: 
    print(f"\n-- Start StateGraph invoke for zone {state['zone']} -- topic [{state['type']}] --\n")
    return {}

def router_route(state: State):
    match state["type"]:
        case "light":
            print("[Router] Routing to: on_light_data")
            return "on_light_data"
        case "air_quality":
            print("[Router] Routing to: on_air_quality_data")
            return "on_air_quality_data"
        case _:
            print(f"[Router] Unexpected mqtt topic message: {state['type']}")
            return "log_error_node"