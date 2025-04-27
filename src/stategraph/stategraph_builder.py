from langgraph.graph                  import StateGraph, START, END
from langgraph.checkpoint.memory      import MemorySaver
from stategraph.state.state           import State
from stategraph.nodes                 import (
    router_route, on_light_data, on_air_quality_data,
    compute_new_temperature, compute_new_humidity, compute_energy_consume,
    vent_action, pump_action, actuate_vent, actuate_pump, log_error_node,
    inject_graph_passive_diffusion
)

def build_stategraph():
    # -- Costruzione StateGraph --
    graph_builder = StateGraph(State)

    # -- Nodi --
    # Separo il nodo per la comunicazione tra grafi dal nodo per recuperare il grafo
    apply_passive_diffusion, set_graph = inject_graph_passive_diffusion()

    nodes = [
        apply_passive_diffusion,
        router_route, 
        on_light_data, 
        on_air_quality_data,
        compute_new_temperature, 
        compute_new_humidity, 
        compute_energy_consume,
        vent_action, 
        pump_action, 
        actuate_vent, 
        actuate_pump,
        log_error_node
    ]

    for node in nodes:
        graph_builder.add_node(node.__name__, node)
    
    # -- Edges --
    graph_builder.add_edge(START, "apply_passive_diffusion")

    graph_builder.add_conditional_edges(
        "apply_passive_diffusion",
        router_route,
        {
            "on_light_data": "on_light_data",
            "on_air_quality_data": "on_air_quality_data",
            "log_error_node": "log_error_node"
        }
    )

    # -- Ramo vent
    graph_builder.add_edge("on_air_quality_data", "vent_action")
    graph_builder.add_edge("on_light_data", "compute_new_temperature")

    graph_builder.add_edge("compute_new_temperature", "vent_action")
    
    graph_builder.add_edge("actuate_vent", "compute_energy_consume")

    # -- Ramo pump
    graph_builder.add_edge("compute_new_temperature", "compute_new_humidity")
    graph_builder.add_edge("compute_new_humidity", "pump_action")

    graph_builder.add_edge("actuate_pump", "compute_energy_consume")

    # -- Ramo finale comune
    graph_builder.add_edge("compute_energy_consume", "log_error_node")
    graph_builder.add_edge("log_error_node", END)

    # -- Compilazione --
    checkpointer = MemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)
    set_graph(graph) # iniezione del grafo che permetterà la comunicazione tra grafi
    return graph
