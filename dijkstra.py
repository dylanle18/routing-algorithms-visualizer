import pandas as pd
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
    history = []

    while pq:
        # Add to history
        dataFrame1 = pd.DataFrame(list(distTo.items()), columns=['Letter', 'DistTo']).replace(float('inf'), "∞")
        dataFrame2 = pd.DataFrame(list(edgeTo.items()), columns=['Letter', 'EdgeTo']).replace(float('inf'), "∞")
        history.append(pd.merge(dataFrame1, dataFrame2, on='Letter', how='outer').set_index('Letter'))

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
    return distTo, edgeTo, history

def get_shortest_path_DJ(graph, start, end):
    distTo, edgeTo, history = dijkstra(graph, start)

    cost = distTo[end]
    shortestPath = []

    while end != start:
        shortestPath.append(end)
        end = edgeTo[end]
    shortestPath.append(start)
    shortestPath = shortestPath[::-1]

    return cost, shortestPath, distTo, edgeTo, history


# Example graph from https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
def main():

    g = Graph([
        Edge('A', 'B', 100),
        Edge('A', 'C', 200),
        Edge('B', 'C', 300),
        Edge('B', 'D', 400),
        Edge('C', 'D', 600),
        Edge('C', 'F', 700),
        Edge('E', 'F', 800)
    ])

    print("Graph:")
    graph = g.to_dict()
    for k, v in graph.items():
        print(k, v)
    print()

    cost, shortestPath, distTo, edgeTo, history = get_shortest_path_DJ(graph, 'A', 'E')
    print("start: A end: E")
    print("cost:", cost)
    print("shortestPath:", shortestPath)
    print("distTo:", distTo)
    print("edgeTo:", edgeTo)
    for h in history:
        print("history:\n", h)


if __name__ == '__main__':
    main()
