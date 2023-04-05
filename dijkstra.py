import heapq
from utils import Edge, Graph


def dijkstra(graph, start):
    # initialize all distances to infinity except the starting node, which has distance 0
    distTo = {node: float('inf') for node in graph}
    distTo[start] = 0

    # initialize the priority queue with the starting node and its distance
    pq = [(0, start)]

    # keep track of visited nodes
    visited = set()

    # keep track of the shortest path to each node
    edgeTo = {}

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
            if dist < distTo[neighbor]:
                # if a shorter path to the neighbor is found, update its distance and path
                distTo[neighbor] = dist
                edgeTo[neighbor] = curr_node
                # add the neighbor to the priority queue with its new distance
                heapq.heappush(pq, (dist, neighbor))

    # return the shortest distances and paths to all nodes
    return distTo, edgeTo


def get_shortest_path_DJ(graph, start, end):
    distTo, edgeTo = dijkstra(graph, start)

    cost = distTo[end]
    shortestPath = []

    while end != start:
        shortestPath.append(end)
        end = edgeTo[end]
    shortestPath.append(start)
    shortestPath = shortestPath[::-1]

    return cost, shortestPath, distTo, edgeTo


# Example graph from https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
def main():
    # graph = {
    #     '0': {'1': 4, '7': 8},
    #     '1': {'0': 4, '2': 8, '7': 11},
    #     '2': {'1': 8, '3': 7, '5': 4, '8': 2},
    #     '3': {'2': 7, '4': 9, '5': 14},
    #     '4': {'3': 9, '5': 10},
    #     '5': {'2': 4, '3': 14, '4': 10, '6': 2},
    #     '6': {'5': 2, '7': 1, '8': 6},
    #     '7': {'6': 1, '0': 8, '1': 11, '8': 7},
    #     '8': {'2': 2, '6': 6, '7': 7},
    # }

    g = Graph([
        Edge('0', '1', 4),
        Edge('0', '7', 8),
        Edge('1', '2', 8),
        Edge('1', '7', 11),
        Edge('2', '3', 7),
        Edge('2', '5', 4),
        Edge('2', '8', 2),
        Edge('3', '4', 9),
        Edge('3', '5', 14),
        Edge('4', '5', 10),
        Edge('5', '6', 2),
        Edge('6', '7', 1),
        Edge('6', '8', 6),
        Edge('7', '8', 7),
    ])

    print("Graph:")
    graph = g.to_dict()
    for k, v in graph.items():
        print(k, v)
    print()

    cost, shortestPath, distTo, edgeTo = get_shortest_path_DJ(graph, '0', '4')
    print("start: 0 end: 4")
    print("cost:", cost)
    print("shortestPath:", shortestPath)
    print("distTo:", distTo)
    print("edgeTo:", edgeTo)


if __name__ == '__main__':
    main()
