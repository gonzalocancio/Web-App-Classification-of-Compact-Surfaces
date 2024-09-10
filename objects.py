# a compact surface can be represented by a regular polygon with an even number of vertices
# where the edges are glued in pairs. Basically it is a directed graph where the underlying
# undirected graph is an even polygon, with the edges grouped in pairs forming a partition of
# the edge set. The direction of the edges gives a direction to the gluing, so it is important
# to keep track of it.
import re

class CompactSurface:
    def __init__(self, vertices, edges, gluing):
        self.vertices = vertices
        self.edges = edges
        self.gluing = gluing

    def __str__(self):
        return f"This surface has {self.vertices} number of vertices, edge set = {self.edges}, and gluing = {self.gluing}"
    # the set of vertices is not important in our implementation. All the information
    # is encoded in the edges and the gluing, so it can be represented by an even positive integer
    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        if not (isinstance(vertices, int) and vertices > 0 and vertices % 2 == 0):
            raise ValueError("Number of vertices must be an even positive integer")
        self._vertices = vertices

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges):
        if not isinstance(edges, set):
            raise TypeError("Edges must be a set of tuples")
        # Handle special cases for the sphere
        if self.vertices == 2:
            if edges == {(0, 1), (0, 1)} or edges == {(1, 0), (1, 0)}:
                self._edges = edges
                return

        valid_edges = set()

        for edge in edges:
            if not (isinstance(edge, tuple) and len(edge) == 2):
                raise ValueError("Each edge must be a tuple of two integers")

            u, v = edge
            if not (isinstance(u, int) and isinstance(v, int)):
                raise ValueError("Vertices in edges must be integers")

            if not (0 <= u < self.vertices and 0 <= v < self.vertices):
                raise ValueError(f"Vertices in edge {edge} must be in range(0, {self.vertices})")

            if not ((u == (v + 1) % self.vertices) or (v == (u + 1) % self.vertices)):
                raise ValueError(f"Edge {edge} is not valid. Edges must be of the form (i, i+1) or (i+1, i)")

            # Check for conflicting edges
            if ((v, u) in valid_edges) and (self.vertices != 2):
                raise ValueError(f"Edges cannot contain both (i, i+1) and (i+1, i) for the same i. Conflicting edge: {(v, u)}")

            valid_edges.add(edge)


        # Ensure each vertex appears in exactly two edges
        vertex_count = {i: 0 for i in range(self.vertices)}
        for u, v in valid_edges:
            vertex_count[u] += 1
            vertex_count[v] += 1

        for count in vertex_count.values():
            if count != 2:
                raise ValueError("Each vertex must appear in exactly two edges")

        self._edges = valid_edges

    @property
    def gluing(self):
        return self._gluing

    @gluing.setter
    def gluing(self, gluing):

        if not isinstance(gluing, set):
            raise TypeError("Gluing must be a set of pairs of edges")
        # Handle special cases for vertices = 2
        if self.vertices == 2:
            if gluing == {((0, 1), (0, 1))} or gluing == {((1, 0), (1, 0))}:
                self._gluing = gluing
                return

        all_glued_edges = set()

        for pair in gluing:
            if not (isinstance(pair, tuple) and len(pair) == 2):
                raise ValueError("Each gluing element must be a tuple of two edges")
            edge1, edge2 = pair
            if not (edge1 in self.edges and edge2 in self.edges):
                raise ValueError("Both edges in a gluing pair must be in the set of edges")
            if edge1 == edge2:
                raise ValueError("Gluing pairs must consist of two distinct edges")

            if edge1 in all_glued_edges or edge2 in all_glued_edges:
                raise ValueError("Each edge must appear in exactly one gluing pair")

            all_glued_edges.add(edge1)
            all_glued_edges.add(edge2)



        if all_glued_edges != self.edges:
            raise ValueError("Gluing must be a partition of the edges, covering all edges exactly once")


        self._gluing = gluing

    def edges_sorted_by_max(self):
    # Identify the special edge
        special_edge = None
        if (self.vertices - 1, 0) in self.edges:
            special_edge = (self.vertices - 1, 0)
        elif (0, self.vertices - 1) in self.edges:
            special_edge = (0, self.vertices - 1)

        # Sort edges by the maximum value of each edge
        sorted_edges = sorted(self.edges, key=lambda edge: max(edge))

        # If we have a special edge, move it to the end of the list
        if special_edge:
            sorted_edges.remove(special_edge)
            sorted_edges.append(special_edge)

        return sorted_edges

    def split_edges(self, edge1, edge2):
        """
        Splits the edges into two lists:
        - list1 contains all edges between edge1 and edge2, not including them.
        - list2 contains all edges from edge2 to edge1, not including them.
        """
        # First, get the sorted list of edges
        sorted_edges = self.edges_sorted_by_max()

        # Ensure that edge1 comes before edge2 in the sorted list
        index1 = sorted_edges.index(edge1)
        index2 = sorted_edges.index(edge2)

        if index1 >= index2:
            raise ValueError("edge1 must come before edge2 in the sorted list of edges.")

        # list1: edges between edge1 and edge2 (excluding edge1 and edge2)
        list1 = sorted_edges[index1 + 1:index2]

        # list2: edges from edge2 to edge1 (excluding edge1 and edge2)
        list2 = sorted_edges[index2 + 1:] + sorted_edges[:index1]

        return list1, list2

    def split_edges_4(self, edge1, edge2, edge3, edge4):
        """
        Splits the edges into four lists:
        - list1 contains all edges between edge1 and edge2, not including them.
        - list2 contains all edges between edge2 and edge3, not including them.
        - list3 contains all edges between edge3 and edge4, not including them.
        - list4 contains all edges from edge4 back to edge1, not including them.
        """
        # Get the sorted list of edges
        sorted_edges = self.edges_sorted_by_max()

        # Ensure that edges are in the correct order in the sorted list
        index1 = sorted_edges.index(edge1)
        index2 = sorted_edges.index(edge2)
        index3 = sorted_edges.index(edge3)
        index4 = sorted_edges.index(edge4)

        if not (index1 < index2 < index3 < index4):
            raise ValueError("Edges must be provided in order, such that edge1 < edge2 < edge3 < edge4 in the sorted list.")

        # List1: edges between edge1 and edge2 (excluding edge1 and edge2)
        list1 = sorted_edges[index1 + 1:index2]

        # List2: edges between edge2 and edge3 (excluding edge2 and edge3)
        list2 = sorted_edges[index2 + 1:index3]

        # List3: edges between edge3 and edge4 (excluding edge3 and edge4)
        list3 = sorted_edges[index3 + 1:index4]

        # List4: edges from edge4 back to edge1 (excluding edge4 and edge1)
        list4 = sorted_edges[index4 + 1:] + sorted_edges[:index1]

        return list1, list2, list3, list4

    def split_edges_general(self, *edges):
        """
        Splits the edges into multiple lists, one list for each segment between consecutive edges.

        Parameters:
        *edges (tuple): A variable number of edges provided as input.

        Returns:
        list of lists: A list containing sublists of edges, where each sublist corresponds to a segment
                    between two consecutive input edges.
        """
        # Get the sorted list of edges
        sorted_edges = self.edges_sorted_by_max()

        # Find the indices of each input edge in the sorted list
        indices = [sorted_edges.index(edge) for edge in edges]

        # Ensure the indices are in strictly increasing order
        if indices != sorted(indices):
            raise ValueError("Input edges must be in the correct order according to the sorted list of edges.")

        # Initialize a list to store the segments
        segments = []

        # Create segments between consecutive edges
        for i in range(len(indices)):
            if i == len(indices) - 1:
                # Last segment: from the last edge back to the first
                segment = sorted_edges[indices[i] + 1:] + sorted_edges[:indices[0]]
            else:
                # Segments between consecutive edges
                segment = sorted_edges[indices[i] + 1:indices[i + 1]]

            # Add the segment to the list of segments
            segments.append(segment)

        return segments




    @classmethod
    # this method will ask the user for the input to construct the compact surface, it will conect with the requirements of the getter functions of the
    # different attributes so that if an error is raised, it will try again, while also giving feedback on the error.
    def get(cls):
        usage_instructions = (
            "Usage: Vertices = 4, \n"
            "Set of edges = {(0, 1), (1, 2), (2, 3), (3, 0)}, \n"
            "Gluing = {((0, 1), (2, 3)), ((1, 2), (3, 0))}"
        )
        while True:
            try:
                vertices = int(input("Number of vertices: "))

                edges_input = input("Set of edges: ")
                edge_pattern = r"\((\d+),\s*(\d+)\)"
                edges = set((int(u), int(v)) for u, v in re.findall(edge_pattern, edges_input))

                gluing_input = input("Gluing: ")
                gluing_pattern = r"\(\((\d+),\s*(\d+)\),\s*\((\d+),\s*(\d+)\)\)"
                gluing = set(((int(u1), int(v1)), (int(u2), int(v2))) for u1, v1, u2, v2 in re.findall(gluing_pattern, gluing_input))

                return cls(vertices, edges, gluing)
            except (ValueError, TypeError, Exception) as e:
                print(f"Error: {e}")
                print(usage_instructions)





