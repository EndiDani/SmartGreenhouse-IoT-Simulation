from langgraph.graph                  import StateGraph, START, END
from langgraph.checkpoint.memory      import MemorySaver
from stategraph.state.state           import State
from stategraph.nodes                 import (
    router, router_route, on_light_data, on_air_quality_data,
    compute_new_temperature, compute_new_humidity, compute_energy_consume,
    vent_action, pump_action, actuate_vent, actuate_pump, log_error_node
)

def build_stategraph():
    # -- Costruzione StateGraph --
    graph_builder = StateGraph(State)

    # -- Nodi --
    nodes = [
        router,
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
    graph_builder.add_edge(START, "router")

    graph_builder.add_conditional_edges(
        "router",
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
    return graph_builder.compile(checkpointer=checkpointer)
