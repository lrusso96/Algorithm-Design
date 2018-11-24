import networkx as nx
from networkx.utils import UnionFind
from math import isnan
from collections import defaultdict

def _has_MST(G, start, end, visited, threshold, debug = False):
    visited.add(start)
    if debug:
        print("DFS hit node", start)
    adj = dict(G.adj[start])
    for n in adj:
        if n in visited or adj[n]["weight"] >= threshold:
            continue
        if n == end:
            return False
        if not _has_MST(G, n, end, visited, threshold):
            return False
    return True        

def has_MST(G, edge, debug = False):
    u,v,w = edge
    w = w["weight"]
    print("check for MST with edge from", u, "to", v, "with weight:", w)
    return _has_MST(G, u, v, set(), w)


def boruvka_mst_edges(G, fixed, debug = False):
    if debug:
        print("Starting Boruvka...")

    # Initialize a forest, assuming initially that it is the discrete
    # partition of the nodes of the graph.
    forest = UnionFind(G)
    
    # Add u and v to the same forest
    yield fixed[0], fixed[1], fixed[2]
    forest.union(fixed[0], fixed[1])  

    def best_edge(component):
        """Returns the optimum (minimum) edge on the edge
        boundary of the given set of nodes.
        A return value of ``None`` indicates an empty boundary."""
        minwt = float('inf')
        boundary = None
        for e in nx.edge_boundary(G, component, data=True):
            wt = e[-1]["weight"]
            if isnan(wt):
                msg = "NaN found as an edge weight. Edge %s"
                raise ValueError(msg % (e,))
            if wt < minwt:
                minwt = wt
                boundary = e
        return boundary

    # Determine the optimum edge in the edge boundary of each component
    # in the forest.
    best_edges = (best_edge(component) for component in forest.to_sets())
    best_edges = [edge for edge in best_edges if edge is not None]

    # If each entry was ``None``, that means the graph was disconnected,
    # so we are done generating the forest.
    while best_edges:
        # Determine the optimum edge in the edge boundary of each
        # component in the forest.
        #
        # This must be a sequence, not an iterator. In this list, the
        # same edge may appear twice, in different orientations (but
        # that's okay, since a union operation will be called on the
        # endpoints the first time it is seen, but not the second time).
        #
        # Any ``None`` indicates that the edge boundary for that
        # component was empty, so that part of the forest has been
        # completed.
        best_edges = (best_edge(component) for component in forest.to_sets())
        best_edges = [edge for edge in best_edges if edge is not None]
        # Join trees in the forest using the best edges, and yield that
        # edge, since it is part of the spanning tree.
        for u, v, d in best_edges:
            if forest[u] != forest[v]:
                yield u, v, d
                forest.union(u, v)

# print the edges of the MST
def weight_of(edges):
    weight = 0
    print("Edges of MST:")
    for e in edges:
        w = e[2]["weight"]
        print(e[0], "->", e[1], "( w:", w ,")")
        weight += w
    return weight

# used to test the algorithm
def build_test_graph():
    G = nx.Graph()
    G.add_edge(1, 2, weight=2)  # specify edge data
    G.add_edge(3, 4, weight=4)  # specify edge data
    G.add_edge(1, 4, weight=3)  # specify edge data
    G.add_edge(2, 4, weight=3)  # specify edge data
    G.add_edge(1, 3, weight=5)  # specify edge data
    return G

def test():
    G = build_test_graph()
    fixed_edges = []
    fixed_edges.append([4,3,{"weight": 4}])
    fixed_edges.append([1,3,{"weight": 5}])
    fixed_edges.append([1,2,{"weight": 2}])
    fixed_edges.append([2,4,{"weight": 3}])
    fixed_edges.append([1,4,{"weight": 3}])

    edges = nx.minimum_spanning_edges(G)
    w = 0
    for e in edges:
        w+= e[2]["weight"]
        
    for fixed in fixed_edges:
        if has_MST(G, fixed):
            edges = boruvka_mst_edges(G, fixed)
            current_w = weight_of(edges)
            if current_w == w:
                print("ok")
            else:
                print(current_w, w)
                raise ValueError()
        else:
            print("no MST!")

