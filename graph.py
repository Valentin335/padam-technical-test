from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

Coordinates = tuple[float, float]
Edge = tuple[int, int, int, Coordinates, Coordinates]

MAX_ANNOTATED_EDGES = 500


class Graph:
    def __init__(
        self,
        vertices: list[Coordinates],
        edges: list[Edge],
    ):
        """Basic constructor of a `Graph` instance.

        Parameters
        ----------
        vertices : list[Coordinates]
            List of vertices coordinates.

        edges : list[Edge]
            List of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges

    def plot(self):
        """
        Plot the graph.
        """
        weights = list(set(edge[2] for edge in self.edges))
        colors = plt.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [
                [edge[-2][::-1], edge[-1][::-1]]
                for edge in self.edges
                if edge[2] == weight
            ]
            ax.add_collection(
                LineCollection(
                    lines, colors=colors(i), alpha=0.7, label=f"weight {weight}"
                )
            )
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()

    @classmethod
    def display_path(cls, *, path: list[Edge]):
        return cls.display_paths(paths=[path])

    @staticmethod
    def display_paths(*, paths: list[list[Edge]]):
        """Display each path, with coordinates swapped as in `plot`.

        Paths up to MAX_ANNOTATED_EDGES edges are drawn as numbered arrows; longer ones
        as segments coloured by order of traversal (thousands of arrows are unreadable
        and very slow to draw).
        """
        colors = plt.get_cmap("viridis", len(paths))
        figure = plt.figure()
        ax = figure.add_subplot()
        for path_index, path in enumerate(paths):
            if len(path) > MAX_ANNOTATED_EDGES:
                lines = LineCollection(
                    [[edge[3][::-1], edge[4][::-1]] for edge in path], cmap="viridis", linewidths=0.6
                )
                lines.set_array(list(range(len(path))))
                ax.add_collection(lines)
                figure.colorbar(lines, ax=ax, label=f"order of traversal (path {path_index})")
                continue
            for edge_index, edge in enumerate(path):
                ax.annotate(
                    str(edge_index),
                    xytext=edge[3][::-1],
                    xy=edge[4][::-1],
                    arrowprops=dict(arrowstyle="->", color=colors(path_index)),
                )
        # annotations do not update the axes limits: fit them to the paths
        ax.update_datalim([coordinates[::-1] for path in paths for edge in path for coordinates in edge[3:5]])
        ax.autoscale_view()
        plt.title(f"{len(paths)} path(s), {sum(len(path) for path in paths)} edges traversed")
        plt.show()
