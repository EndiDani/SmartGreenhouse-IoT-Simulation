from   stategraph.stategraph_builder import build_stategraph
import os 

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__),)
    output_path = os.path.join(BASE_DIR, "graph.png")  

    img_data = build_stategraph().get_graph().draw_mermaid_png()

    with open(output_path, "wb") as f:
        f.write(img_data)
        
except Exception as e:
    print(f"Errore: {e}")