from stategraph.state.state import State 

def log_error_node(state: State) -> State: 
    if state["events"] is not None: 
        print("\n[ERRORS DETECTED]\n")
        for err in state["events"]: 
            print(f"-> [{err}]")
        state["events"].clear()
    return state