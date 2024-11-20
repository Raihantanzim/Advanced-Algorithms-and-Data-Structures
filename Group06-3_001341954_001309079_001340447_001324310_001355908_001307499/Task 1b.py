import csv
import networkx as nx
import matplotlib.pyplot as plt

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

        G = nx.Graph()

        for row in reader:
            station_a, station_b, travel_time = row

            # Add stations to the dictionary if they don't exist
            if station_a not in stations:
                stations[station_a] = station_index
                station_index += 1

            if station_b not in stations:
                stations[station_b] = station_index
                station_index += 1

            G.add_edge(station_a, station_b, weight=int(travel_time))

    return G, stations

def analyze_edges(G):
  """
  Analyzes the number of edges for a given graph.

  Args:
      G (nx.Graph): The NetworkX graph object.

  Returns:
      int: The total number of edges in the graph.
  """
  return G.number_of_edges()

def plot_analysis(num_stations, num_edges):
  """
  Plots the number of edges vs. number of stations.

  Args:
      num_stations (list): A list of station counts (x-axis data).
      num_edges (list): A list of edge counts (y-axis data).
  """
  plt.plot(num_stations, num_edges, marker= 'o', label='Number of Edges')
  plt.xlabel('Number of Minutes')
  plt.ylabel('Number of Stations')
  plt.title('Relationship between Stations and Edges')
  plt.legend()
  plt.grid(True)
  plt.show()

def main():
  # Replace with actual data for stations and edges (can be from a loop)
  num_stations = [0,10, 20, 30, 40, 50]  # Sample station counts
  num_edges = []
  for n in num_stations:
    # Create a sample graph with n stations
    G = nx.random_geometric_graph(n, 0.5)
    num_edges.append(analyze_edges(G))

  plot_analysis(num_stations, num_edges)

if __name__ == "__main__":
  main()
