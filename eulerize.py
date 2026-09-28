import numpy as np
import pymatching

from graph import Graph


def edges_to_duplicate(graph: Graph) -> list:
    """Cheapest edges to traverse a second time so that the connected graph keeps at
    most 2 odd-degree vertices: then it has an Eulerian path (see `eulerian_path`).

    Duplicating the edges of a path between two odd vertices makes both of them even,
    and leaves the parity of the intermediate vertices unchanged. So the odd vertices
    are paired by a minimum-weight perfect matching (Blossom), each pair being linked by
    a shortest path. PyMatching solves it directly on the sparse graph and returns the
    edges to duplicate, i.e. the cheapest edge set making every given vertex even.

    Open path: two dummy vertices s and t, linked to every odd vertex, must also become
    even, i.e. each gets an odd number of chosen edges. The vertex a dummy vertex is linked
    to stays odd: it is the start or the end of the path. An edge to a dummy vertex costs W,
    the sum of the weights: linking a dummy vertex to 3 vertices instead of 1 costs 2W more,
    while freeing 2 more vertices saves at most one shortest path, which is at most W. So
    each dummy vertex takes exactly one edge.
    """
    degree = {}
    for edge in graph.edges:
        degree[edge[0]] = degree.get(edge[0], 0) + 1
        degree[edge[1]] = degree.get(edge[1], 0) + 1
    odd_vertices = [vertex for vertex, d in degree.items() if d % 2 == 1]
    if len(odd_vertices) <= 2:
        return []

    dummy_s, dummy_t = len(graph.vertices), len(graph.vertices) + 1
    dummy_weight = sum(edge[2] for edge in graph.edges)

    matching = pymatching.Matching()
    for index, edge in enumerate(graph.edges):
        # between parallel edges, the cheapest one is duplicated
        matching.add_edge(edge[0], edge[1], fault_ids={index}, weight=edge[2], merge_strategy="smallest-weight")
    for vertex in odd_vertices:
        matching.add_edge(dummy_s, vertex, weight=dummy_weight)  # no fault id: not an edge of the graph
        matching.add_edge(dummy_t, vertex, weight=dummy_weight)

    to_make_even = np.zeros(len(graph.vertices) + 2, dtype=np.uint8)
    to_make_even[odd_vertices + [dummy_s, dummy_t]] = 1
    chosen = matching.decode(to_make_even)
    return [graph.edges[index] for index in np.flatnonzero(chosen)]
