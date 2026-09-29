from instance import Instance


def check(instance: Instance, paths: list[list]):
    """Check that `paths` is a valid answer for `instance`, independently of the solver.

    - each path is contiguous: every edge starts where the previous one ends;
    - every traversed edge exists in the instance, with its weight;
    - every edge of the instance is traversed at least once;
    - one path per connected component, each path staying in its component.

    Raises ValueError on the first violated rule, otherwise prints the cost next to the
    lower bound W (sum of the weights: every edge has to be traversed at least once).
    """

    def key(edge):
        return min(edge[0], edge[1]), max(edge[0], edge[1]), edge[2]

    instance_edges = {key(edge) for edge in instance.edges}

    for path_index, path in enumerate(paths):
        for step, edge in enumerate(path):
            if step > 0 and path[step - 1][1] != edge[0]:
                raise ValueError(
                    f"path {path_index}, step {step}: starts at {edge[0]} "
                    f"but the previous edge ends at {path[step - 1][1]}"
                )
            if key(edge) not in instance_edges:
                raise ValueError(
                    f"path {path_index}, step {step}: edge {edge[0]}-{edge[1]} "
                    f"with weight {edge[2]} is not in the instance"
                )

    traversed = {key(edge) for path in paths for edge in path}
    uncovered = sorted(instance_edges - traversed)
    if uncovered:
        raise ValueError(f"{len(uncovered)} edges never traversed, e.g. {uncovered[:3]}")

    # connected components with a union-find, not shared with the solver
    parent = {}

    def find(vertex):
        parent.setdefault(vertex, vertex)
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in instance.edges:
        parent[find(edge[0])] = find(edge[1])
    components = {find(edge[0]) for edge in instance.edges}

    path_components = []
    for path_index, path in enumerate(paths):
        roots = {find(vertex) for edge in path for vertex in edge[:2]}
        if len(roots) != 1:
            raise ValueError(f"path {path_index} goes through {len(roots)} connected components")
        path_components.append(roots.pop())
    if sorted(path_components) != sorted(components):
        raise ValueError(f"{len(paths)} paths for {len(components)} connected components, expected one each")

    cost = sum(edge[2] for path in paths for edge in path)
    lower_bound = sum(edge[2] for edge in instance.edges)
    print(
        f"Check OK: {len(paths)} path(s) covering the {len(instance_edges)} edges, "
        f"cost {cost} >= lower bound {lower_bound} (+{100 * (cost - lower_bound) / lower_bound:.1f}%)"
    )
