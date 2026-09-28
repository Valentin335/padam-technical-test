from graph import Graph


def eulerian_path(graph: Graph) -> list:
    """Eulerian path: a path traversing every edge of the connected graph exactly once.

    It is the greedy of `example_solution` plus a splicing step: when the walk gets stuck
    while edges remain, it resumes from a vertex of the walk that still has unused edges,
    and the new sub-circuit is inserted there. The stack performs this splicing
    implicitly: a vertex is written to the path only once all its edges are used, so the
    path is built backwards.

    The graph must have 0 odd-degree vertex (the path is a circuit) or 2 (the path goes
    from one to the other). Edges are identified by their index, so an edge given twice
    in `graph.edges` is traversed twice.
    """
    incident_edges = {}  # vertex -> indices in graph.edges of its edges
    for index, edge in enumerate(graph.edges):
        incident_edges.setdefault(edge[0], []).append(index)
        incident_edges.setdefault(edge[1], []).append(index)

    odd_vertices = [vertex for vertex, indices in incident_edges.items() if len(indices) % 2 == 1]
    if len(odd_vertices) > 2:
        raise ValueError(f"{len(odd_vertices)} odd-degree vertices, no Eulerian path")
    start = odd_vertices[0] if odd_vertices else graph.edges[0][0]

    used = [False] * len(graph.edges)
    stack = [(start, None)]  # (vertex, index of the edge used to reach it)
    reversed_path = []
    while stack:
        vertex, reached_by = stack[-1]
        while incident_edges[vertex] and used[incident_edges[vertex][-1]]:
            incident_edges[vertex].pop()  # already used from its other endpoint

        if incident_edges[vertex]:  # walk forward along an unused edge
            index = incident_edges[vertex].pop()
            used[index] = True
            edge = graph.edges[index]
            next_vertex = edge[1] if edge[0] == vertex else edge[0]
            stack.append((next_vertex, index))
        else:  # stuck: `vertex` ends what remains of the path
            stack.pop()
            if reached_by is not None:
                previous_vertex = stack[-1][0]
                reversed_path.append(
                    (
                        previous_vertex,
                        vertex,
                        graph.edges[reached_by][2],
                        graph.vertices[previous_vertex],
                        graph.vertices[vertex],
                    )
                )

    if not all(used):
        raise ValueError("graph is not connected")
    return reversed_path[::-1]
