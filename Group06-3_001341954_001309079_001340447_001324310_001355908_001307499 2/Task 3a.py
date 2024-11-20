import openpyxl
import queue  # Importing the queue module for PriorityQueue
import matplotlib.pyplot as plt
from tkinter import Tk



def load_underground_data():
    """
    Loads London Underground data from an Excel file using a file dialog.
    Returns the graph representation and the file path.
    """
    Tk().withdraw()  # Suppress the tkinter root window

    file_path = r"London Underground data.xlsx"

    print(f"Loading data from: {file_path}")

    # Load workbook and create graph
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    graph = {}

    # Process Excel data starting from row 3
    for row in sheet.iter_rows(min_row=3, max_col=4, values_only=True):
        line, station1, station2, duration = row
        if station1 and station2 and duration:
            for station in (station1, station2):
                if station not in graph:
                    graph[station] = {}
            graph[station1][station2] = duration
            graph[station2][station1] = duration

    print(f"Loaded {len(graph)} stations")
    return graph, file_path


def dijkstra(graph, start):
    """
    Implementation of Dijkstra's algorithm using queue.PriorityQueue.
    Returns distances and paths to all stations from the start station.
    """
    distances = {node: float('inf') for node in graph}
    paths = {node: [] for node in graph}
    distances[start] = 0
    paths[start] = [start]

    pq = queue.PriorityQueue()  # Use PriorityQueue from queue module
    pq.put((0, start))  # (distance, station)

    while not pq.empty():
        current_distance, current_station = pq.get()

        if current_distance > distances[current_station]:
            continue

        for neighbor, weight in graph[current_station].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = paths[current_station] + [neighbor]
                pq.put((distance, neighbor))

    return distances, paths


def calculate_all_journeys(graph):
    """
    Calculates all possible journeys in the network, excluding duplicate pairs.
    Returns journey durations and details of the longest journey.
    """
    stations = list(graph.keys())
    n = len(stations)
    print(f"Calculating journeys for {n} stations...")
    print(f"Expected number of journeys: {n * (n - 1)}")

    all_durations = []
    longest_journey = {
        'duration': 0,
        'start': None,
        'end': None,
        'path': None
    }

    for start in stations:
        distances, paths = dijkstra(graph, start)

        for end in stations:
            if start != end and distances[end] < float('inf'):
                # Ensure journey direction is only counted once (A to B, not B to A)
                if start < end:
                    duration = distances[end]
                    all_durations.append(duration)

                    # Update longest journey if current is longer
                    if duration > longest_journey['duration']:
                        longest_journey.update({
                            'duration': duration,
                            'start': start,
                            'end': end,
                            'path': paths[end]
                        })

    print(f"Total journeys calculated: {len(all_durations)}")
    return all_durations, longest_journey


def plot_journey_histogram(durations):
    """
    Creates and displays a histogram of journey durations.
    """
    plt.figure(figsize=(12, 6))
    plt.hist(durations, bins=50, color='skyblue', edgecolor='black')
    plt.title('Distribution of London Underground Journey Durations')
    plt.xlabel('Journey Duration (minutes)')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.show()


def main():
    try:
        # 1. Load the Underground network data
        print("\n1. Loading London Underground Data")
        graph, file_path = load_underground_data()

        # 2. Calculate all possible journeys
        print("\n2. Calculating All Possible Journeys")
        durations, longest_journey = calculate_all_journeys(graph)

        # 3. Display journey statistics
        print("\n3. Journey Statistics")
        print(f"Total number of stations: {len(graph)}")
        print(f"Total number of journeys calculated: {len(durations)}")
        print(f"Average journey duration: {sum(durations) / len(durations):.2f} minutes")

        # 4. Display longest journey details
        print("\n4. Longest Journey Details")
        print(f"Start Station: {longest_journey['start']}")
        print(f"End Station: {longest_journey['end']}")
        print(f"Duration: {longest_journey['duration']} minutes")
        print("Path:")
        print(" -> ".join(longest_journey['path']))

        # 5. Plot histogram
        print("\n5. Generating Histogram")
        plot_journey_histogram(durations)

    except Exception as e:
        print(f"\nError: {str(e)}")
        return


if __name__ == "__main__":
    main()
