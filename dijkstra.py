import heapq


def dijkstra(graph, start):
    # initialize all distances to infinity except the starting node, which has distance 0
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # initialize the priority queue with the starting node and its distance
    pq = [(0, start)]

    # keep track of visited nodes
    visited = set()

    # keep track of the shortest path to each node
    path = {}

    while pq:
        # get the node with the shortest distance from the priority queue
        (curr_dist, curr_node) = heapq.heappop(pq)

        # if the node has already been visited, skip it
        if curr_node in visited:
            continue

        # mark the node as visited
        visited.add(curr_node)

        # update the distances to the neighbors of the current node
        for neighbor, weight in graph[curr_node].items():
            dist = curr_dist + weight
            if dist < distances[neighbor]:
                # if a shorter path to the neighbor is found, update its distance and path
                distances[neighbor] = dist
                path[neighbor] = curr_node
                # add the neighbor to the priority queue with its new distance
                heapq.heappush(pq, (dist, neighbor))

    # return the shortest distances and paths to all nodes
    return distances, path


# Example graph from https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
graph = {
    '0': {'1': 4, '7': 8},
    '1': {'0': 4, '2': 8, '7': 11},
    '2': {'1': 8, '3': 7, '5': 4, '8': 2},
    '3': {'2': 7, '4': 9, '5': 14},
    '4': {'3': 9, '5': 10},
    '5': {'2': 4, '3': 14, '4': 10, '6': 2},
    '6': {'5': 2, '7': 1, '8': 6},
    '7': {'6': 1, '0': 8, '1': 11, '8': 7},
    '8': {'2': 2, '6': 6, '7': 7},
}

start = '0'

distances, path = dijkstra(graph, start)

print("Shortest Distances:")
for node, distance in distances.items():
    print(f"{node}: {distance}")

print("\nShortest Paths:")
for node, parent in path.items():
    print(f"{node} <- {parent}")
