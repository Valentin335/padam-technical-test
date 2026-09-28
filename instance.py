from __future__ import annotations

from graph import Coordinates, Edge, Graph


class Instance:
    def __init__(
        self,
        vertices: list[Coordinates],
        edges: list[Edge],
    ):
        """An instance read from a file: it may contain several connected graphs.

        Parameters
        ----------
        vertices : list[Coordinates]
            List of vertices coordinates.

        edges : list[Edge]
            List of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges

    def connected_components(self) -> list[Graph]:
        """Split the instance into its connected components (breadth-first search).

        Returns
        -------
        list[Graph]
            One connected graph per component, sharing the vertices list of the instance
            and keeping only its own edges. Isolated vertices are ignored.
        """
        incident_edges = {}
        for edge in self.edges:
            incident_edges.setdefault(edge[0], []).append(edge)
            incident_edges.setdefault(edge[1], []).append(edge)

        visited, components = set(), []
        for source in incident_edges:
            if source in visited:
                continue
            visited.add(source)
            queue, component_edges = [source], set()
            for vertex in queue:  # `queue` grows during the loop
                for edge in incident_edges[vertex]:
                    component_edges.add(edge)
                    neighbour = edge[1] if edge[0] == vertex else edge[0]
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
            edges = [edge for edge in self.edges if edge in component_edges]
            components.append(Graph(self.vertices, edges))
        return components
