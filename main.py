from input import parse_cmd_line, parse_file
from graph import Graph
from instance import Instance
from example_solution import solve, print_paths
from checker import check


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    instance = Instance(vertices, edges)

    paths = solve(instance)
    print_paths(paths)
    check(instance, paths)

    if plot_graph:
        Graph(vertices, edges).plot()
        Graph.display_paths(paths=paths)


if __name__ == "__main__":
    main()
