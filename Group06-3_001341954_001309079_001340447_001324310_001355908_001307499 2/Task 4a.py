import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from min_heap_priority_queue import MinHeapPriorityQueue
from mst import kruskal


def prim(G, r):
    """Return the minimum spanning tree of a weighted, undirected graph G using Prim's algorithm.

    Arguments:
    G -- an undirected graph, represented by adjacency lists
    r -- root vertex to start from
    """
    # Initialize keys and predecessors.
    card_V = G.get_card_V()
    pi = [None] * card_V
    visited = [False] * card_V  # visited vertices are in the MST
    key = [float('inf')] * card_V  # vertices not yet in MST
    key[r] = 0  # root r has key 0

    # Initialize the min-priority queue of vertices.
    queue = MinHeapPriorityQueue(lambda u: key[u])
    for u in range(card_V):
        queue.insert(u)

    while queue.get_size() > 0:
        u = queue.extract_min()  # add u to the tree
        visited[u] = True
        for edge in G.get_adj_list(u):  # update the keys of u's non-tree neighbors
            v = edge.get_v()
            weight = edge.get_weight()
            if not visited[v] and weight < key[v]:  # update v's key?
                pi[v] = u
                key[v] = weight
                queue.decrease_key(v, weight)  # update v in the min-priority queue

    # Make the MST as an undirected, weighted graph.
    mst = AdjacencyListGraph(card_V, False, True)
    for i in range(card_V):
        # Insert edges from vertices and their predecessors.
        if pi[i] is not None:
            mst.insert_edge(pi[i], i, key[i])

    return mst

def get_total_weight(G):
    """Return the total weight of edges in an undirected graph G."""
    total_weight = 0
    for u in range(G.get_card_V()):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                total_weight += edge.get_weight()
    return total_weight

def print_working_stations(G, vertices):
    """Print the working stations in an undirected graph G."""
    working_stations = set()
    for u in range(G.get_card_V()):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                working_stations.update([vertices[u], vertices[v]])
    for station in sorted(working_stations):
        print(station)

# Load and Process London Underground Data
if __name__ == "__main__":
    # Load the data
    file_path = 'London Underground data.xlsx'  # ADJUST FILE PATH
    df = pd.read_excel(file_path, sheet_name='Sheet1')  # LOAD EXCEL DATA

    # Parse data into a graph format
    stations = set()
    edges = []
    for i in range(len(df) - 1):
        line = df.iloc[i, 0]
        station1 = df.iloc[i, 1]
        station2 = df.iloc[i + 1, 1]

        # If next station is on the same line, add edge
        if df.iloc[i + 1, 0] == line:
            stations.update([station1, station2])
            edges.append((station1, station2, 1))  # Assuming weight is 1

    # Create station index mapping
    station_to_index = {station: idx for idx, station in enumerate(stations)}

    # Build graph
    num_stations = len(stations)
    graph = AdjacencyListGraph(num_stations, False, True)

    for station1, station2, weight in edges:
        # Skip self-loops
        if station1 != station2 and not graph.has_edge(station_to_index[station1], station_to_index[station2]):
            graph.insert_edge(station_to_index[station1], station_to_index[station2], weight)

    # Run MST Algorithms
    print("Launching Kruskal's MST on London Underground data:")
    kruskal_mst = kruskal(graph)
    print("Working stations in Kruskal's MST:")
    print_working_stations(kruskal_mst, list(station_to_index.keys()))
    print("Total weight of Kruskal's MST:", get_total_weight(kruskal_mst))

    print("\nRunning Prim's MST on London Underground data:")
    prim_mst = prim(graph, 0)
    print("Working stations:")
    print_working_stations(prim_mst, list(station_to_index.keys()))
    print("Total weight:", get_total_weight(prim_mst))

    # Optional: Identify removable edges
    original_edges = set(graph.get_edge_list())
    mst_edges = set(kruskal_mst.get_edge_list())
    removable_edges = original_edges - mst_edges
    print("\nShutdown Edges:")
    for u, v in removable_edges:
        print(f"{list(station_to_index.keys())[u]} -- {list(station_to_index.keys())[v]}")
