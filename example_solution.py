from graph import Graph


def example_solution(graph: Graph) -> list:
    """Implement a naive solution to find a path in the graph which travels all edges."""
    uncovered_edges = set(graph.edges)
    current_vertex = graph.edges[0][0]  # Pick a starting vertex (of this component)
    path = []

    while uncovered_edges:
        # Find an edge not yet covered and incident to the current vertex
        next_vertex = None
        for edge in uncovered_edges:
            if current_vertex in edge[:2]:
                next_vertex = edge[1] if edge[0] == current_vertex else edge[0]
                break

        if next_vertex is not None:  # vertex 0 is a valid next vertex
            path.append(
                (
                    current_vertex,
                    next_vertex,
                    edge[2],
                    graph.vertices[current_vertex],
                    graph.vertices[next_vertex],
                )
            )
            uncovered_edges.remove(edge)
            current_vertex = next_vertex
        else:
            print("Problem detected: need to exit to avoid infinite loop.")
            break

    return path
