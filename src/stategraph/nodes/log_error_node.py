from stategraph.state.state      import State 
from stategraph.nodes.print_lock import print_lock

def log_error_node(state: State) -> State: 
    steps_to_add = []

    if state["events"]: 
        steps_to_add.append("[ERRORS DETECTED]\n")
        for err in state["events"]: 
            steps_to_add.append(f"-> [{err}]")
        state["events"].clear()

    # Stampo tutti gli step del grafo con lock in modo che sia sequenziale
    with print_lock: 
        for step in (state["steps"] + steps_to_add): 
            print(f"{step}")

    state["steps"].clear()

    return {
        "steps": state["steps"],
        "events": state["events"]
    }