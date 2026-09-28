from graph import Graph
from instance import Instance


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


def solve(instance: Instance) -> list[list]:
    """Compute one path per connected component of the instance."""
    components = instance.connected_components()
    if len(components) > 1:
        print(f"Warning: {len(components)} connected components, one path per component is computed.")

    paths = []
    for index, component in enumerate(components):
        path = example_solution(component)
        covered = {(min(edge[0], edge[1]), max(edge[0], edge[1]), edge[2]) for edge in path}
        print(f"Component {index}: #E={len(component.edges)}, covered edges={len(covered)}/{len(component.edges)}")
        paths.append(path)
    return paths


def print_paths(paths: list[list]):
    """Print the length and value of each path, then the total value."""
    for index, path in enumerate(paths):
        print(f"Path {index}: length of path found={len(path) + 1}, value of path found={sum(edge[2] for edge in path)}")
    print("Total value of paths found:", sum(edge[2] for path in paths for edge in path))
