import json
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Port:
    name: str
    vertices: List[Tuple[float, float]]
    edges: List[Tuple[Tuple[float, float], Tuple[float, float]]]

def load_ports(json_file_path):
    # Load JSON data from the file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Extract the list of Port objects
    ports = [
        Port(name=port_data["name"],
                vertices=[(point["lat"], point["long"]) for point in port_data["points"]],
                edges=create_edges_from_vertices([(point["lat"], point["long"]) for point in port_data["points"]])
                ) for port_data in data
    ]

    return ports

def create_edges_from_vertices(vertices):
    edges = []
    for i in range(len(vertices) - 1):
        edge = (vertices[i], vertices[i + 1])
        edges.append(edge)
    # Connect the last and first vertices to close the polygon
    edges.append((vertices[-1], vertices[0]))
    return edges

def is_inside(edges, xp, yp):
    cnt = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        if (yp < y1) != (yp < y2) and xp < x1 + ((yp-y1)/(y2-y1))*(x2-x1):
            cnt += 1
    return cnt%2 == 1