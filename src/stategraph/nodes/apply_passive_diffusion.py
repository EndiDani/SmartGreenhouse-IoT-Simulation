from stategraph.state.state import State
import asyncio

# Rendo asincrona la chiamata a get_state in modo da leggere in parallelo piu stati
async def get_state_async(graph, config):
    loop = asyncio.get_running_loop()
    state_snapshot = await loop.run_in_executor(None, graph.get_state, config)
    return state_snapshot.values

def inject_graph_passive_diffusion(): 
    graph_ref = {}
    
    async def apply_passive_diffusion(state: State) -> State: 
        graph         = graph_ref["graph"]
        events_to_add = []
        steps_to_add  = []
        delta_temp    = 0
        delta_hum     = 0
        
        # Prints del primo nodo
        steps_to_add.append(f"------ Zone {state['zone']} on topic [{state['type']}] ------\n")
        steps_to_add.append(
            "Actual state:\n\n" + "\n".join(
                f"{k}: {v}" for k, v in state.items() if k not in ("zone", "env", "events", "steps", "type")
            ) + "\n"
        )

        try: 
            tasks = [
                get_state_async(graph, {"configurable": {"thread_id": neighbor}})
                for neighbor in state["neighbors"]
            ]

            neighbor_states = await asyncio.gather(*tasks)
            len_neighbor_state = len(neighbor_states)
            steps_to_add.append(f"[apply_passive_diffusion] received {len_neighbor_state} neighbor_states")

            for neighbor_state in neighbor_states:
                if neighbor_state: 
                    delta_temp += neighbor_state["thermometer"] - state["thermometer"]
                    delta_hum  += neighbor_state["humidity"] - state["humidity"]
            # Normalizzo i delta per zone che confinano con più zone
            if len_neighbor_state > 0: 
                delta_temp /= len_neighbor_state 
                delta_hum /= len_neighbor_state 
            
            # Moltiplico per i coefficienti per adattare il delta alla serra
            delta_temp *= state["env"]["k_temp"]
            delta_hum *= state["env"]["evap_coeff"]

            steps_to_add.append(f"[apply_passive_diffusion] Temperature influence: {delta_temp}")
            steps_to_add.append(f"[apply_passive_diffusion] Humidity influence: {delta_hum}")
        except Exception as e:  
            events_to_add.append(f"Error in communication between zones, from zone {state['zone']} -- {e}")

        state["thermometer"] += delta_temp
        state["humidity"] += delta_hum
        
        return {
            "thermometer": state["thermometer"], 
            "humidity": state["humidity"], 
            "steps": steps_to_add, 
            "events": events_to_add
        }

    def set_graph(graph): 
        graph_ref["graph"] = graph
    
    return apply_passive_diffusion, set_graph