from copy import deepcopy
from typing import Dict, Union


class Graph:
    """Representation of a simple graph using an adjacency map.
    Adjacency Map Structure implemented with hash tables.
    """

    # nested Vertex class
    class Vertex:
        """Lightweight vertex structure for a graph"""
        __slots__ = '_element'

        def __init__(self, x):
            """Do not call constructor directly. 
            Use Graph's insert_vertex(x)."""
            self._element = x

        def __str__(self):
            return str(self._element)
        
        def __repr__(self):
            return str(self._element)
        
        def element(self):
            """Return element associated with this vertex."""
            return self._element

        def __hash__(self):
            # will allow vertex to be a map/set key
            return hash(id(self))

    # nested Edge class
    class Edge:
        """lightweight edge structure for a graph"""
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, x):
            """Do not call constructor directly.
            Use Graph's insert_edge(u, v, x)"""
            self._origin = u
            self._destination = v
            self._element = x

        def __str__(self):
            return f"{self._origin}-({self._element})-{self._destination}"
        
        def __repr__(self):
            return f"{self._origin}-({self._element})-{self._destination}"

        def endpoint(self):
            """Return (u, v) tuple for vertices u and v"""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Return the vertex that is opposite v on the edge"""
            return self._destination if v is self._origin else self._origin

        def element(self):
            """Return element associated with this edge"""
            return self._element
        
        def __hash__(self):
            # will allow edge to be a map/set key
            return hash((self._origin, self._destination))


    def __init__(self, directed=False):
        """Create an empty graph(undirected by default)
        Graph is directed if optional parameter is set to True"""
        self._outgoing = {}
        # only create second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        """Return True if this is a directed graph; False if undirected.
        Property is based on the original declaration of the graph,
        not its content"""
        # directed if maps are distinct
        return self._incoming is not self._outgoing

    def vertex_count(self):
        """Return the number of vertives in the graph"""
        return len(self._outgoing)

    def vertices(self):
        """Return an iteration of all vertices of the graph"""
        return list(self._outgoing.keys())

    def edge_count(self):
        """Return the number of edges in the graph"""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges"""
        return total if self.is_directed() else total // 2

    def edges(self):
        """Return a set of all edges of the graph"""
        # avoid double-reporting edges of undirected graph
        result = set()
        for secondary_map in self._outgoing.values():
            # add edges to resulting set
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """Return the edge from u to v, or None if not adjacent"""
        # return None if v not adjacent
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """Return number of (outgoing) edges incident to vertex v
        in the graph. If graph is directed, optional parameter 
        used to count incoming edges"""

        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """Return all(outgoing) edges incident to vertex v in
        the graph. If graph is directed, optional parameter used
        to request incoming edges"""
        adj = self._outgoing if outgoing else self._incoming
        for edges in adj[v].values():
            yield edges
        
    def insert_vertex(self, x=None):
        """Insert and return a new Vertex with element x"""
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v
    
    def insert_edge(self, u, v, x=None):
        """Insert and return a new Edge from u to v with auxliary element x"""
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e
    
    def remove_vertex(self, v):
        """InserDeltet and return the Vertex v
        Raise KeyError is v not in graph.
        """
        if v not in self._outgoing:
            raise KeyError('Key Error ' + repr(v))
        del self._outgoing[v]
        if self.is_directed():
            del self._incoming[v]
        return v

    def remove_edges(self, e):
        """Delete adn return edge e from graph"""
        u, v = e._origin, e._destination
        del self._outgoing[u][v]
        del self._incoming[v][u]
        return e

    def dfs(self, u):
        """Perform DFS of the undiscovered portion of Graph g
        starting at Vertex u.

        Discovered is a dictionary mapping each vertex to the
        edge that was used to discover it during the DFS(u should
        be "discovered" prior to the call.)Newly discovered vertices
        will be added to the dictionary as a result."""

        # typing of discovered
        VE = Dict[self.Vertex, Union[self.Edge, None]]
        # here we use closure to save dfs path
        # with u trivially discovered
        discovered: VE = {u: None}
        # traverse the graph
        def _dfs(u):
            # for every outgoing edge from u
            for e in self.incident_edges(u):
                v = e.opposite(u)
                # v is an unvisited vertex
                if v not in discovered:
                    # e is the tree edge that discovered v
                    discovered[v] = e
                    # recursively explore from v
                    _dfs(v)
        # call it
        _dfs(u)
        return discovered
        
    # Reconstructing a Path from u to v
    def construct_path(self, u, v, dfs=True):
        if dfs:
            discovered = self.dfs(u)
        else:
            discovered = self.bfs(u)
        # empty path by default
        path = []
        if v in discovered:
            # we build list from v to u and then revese it at the end
            path.append(v)
            walk = v
            while walk is not u:
                e = discovered[walk]
                parent = e.opposite(walk)
                path.append(parent)
                walk = parent
            # rotate path from u to v
            path.reverse()
        return path

    def dfs_complete(self):
        """Perform DFS for entire graph and return forest as a dictionary.

        Result maps each vertex v tp the edge that was used to discover it.
        (Vertices that are roots of a DFS tree are mapped to None)"""
        forest = {}
        for u in self.vertices():
            if u not in forest:
                # u will be the root of a tree
                forest[u] = None
                self.dfs(u)
        return forest

    def bfs(self, s):
        """Perform BFS of the undiscovered portion of Graph g starting at
        Vertex s.

        discovered is a dictionary mapping each vertex to the edge that 
        was used to discover it during the BFS(s should be mapped to None
        prior to the call). Newly discovered vertices will be added to the
        dictionary as a result."""
        discovered = {s: None}
        # first level includes only s
        level = [s]
        while len(level) > 0:
            # prepateto gather newly found vertices
            next_level = []
            for u in level:
                # for every outgoing edge from u
                for e in self.incident_edges(u):
                    v = e.opposite(u)
                    # v is an unvisited vertex
                    if v not in discovered:
                        # e is the edge that discovered v
                        discovered[v] = e
                        # v will be further considered in next pass
                        next_level.append(v)
            # relabel 'next' level to become current
            level = next_level
        return discovered

    # Floyd-Warshall algorithm
    def floyd_warshall(self):
        """Return a new graph that is the transitive closure of g"""
        closure = deepcopy(self)
        # make indexable list
        verts = closure.vertices()
        n = len(verts)
        for k in range(n):
            for i in range(n):
                # verify that edge (i, k) exists in the partial closure
                if i != k and closure.get_edge(verts[i], verts[k]) is not None:
                    for j in range(n):
                        # verify that edge(k, j) exists in the partial closure
                        if i != j != k and closure.get_edge(verts[k], verts[j]):
                            # if (i, j) not yet included, add it to the closure
                            if closure.get_edge(verts[i], verts[j]) is None:
                                closure.insert_edge(verts[i], verts[j])
