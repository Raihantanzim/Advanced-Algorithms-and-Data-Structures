from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph
import csv

def create_graph(csv_file):
    """
    Creates a graph from a CSV file containing station information.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing the graph and a dictionary mapping station names to indices.
    """

    stations = {}
    station_index = 0

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row

        # Create a list to store edges
        edges = []

        for row in reader:
            station_a, station_b, travel_time = row

            # Add stations to the dictionary if they don't exist
            if station_a not in stations:
                stations[station_a] = station_index
                station_index += 1

            if station_b not in stations:
                stations[station_b] = station_index
                station_index += 1

            edges.append((stations[station_a], stations[station_b], int(travel_time)))

    # Create the graph with the correct size
    graph = AdjacencyListGraph(len(stations), True, True)

    # Add edges to the graph
    for u, v, w in edges:
        graph.insert_edge(u, v, w)

    return graph, stations

def find_shortest_path(graph, stations, start, end):
    # Starting an empty path and setting the current node to the end station
    path, current = [], stations[end]

    # Applying Dijkstra's algorithm to find the shortest path
    distances, predecessors = dijkstra(graph, stations[start])

    # Backtracking from the end station to the start station
    while current != None:
        # Inserting the station name at the beginning of the path
        path.insert(0, next(station for station, idx in stations.items() if idx == current))
        # Moves to the predecessor of the current node
        current = predecessors[current]

    return path, distances[stations[end]]

def main():
    # Loading graph and stations dictionary
    graph, stations = create_graph('london_underground_graph.csv')

    # Asking the user to enter his start and his destination
    start, end = input("Enter start station: "), input("Enter end station: ")

    # Finding the shortest path between the start and end
    path, time = find_shortest_path(graph, stations, start, end)

    # Showing the path and total travel time
    print(f"Path: {' -> '.join(path)}\nDuration: {time} minutes")

if __name__ == "__main__":
    main()
