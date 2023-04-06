import pandas as pd

class Edge:
    def __init__(self, n1 : str, n2 : str, cost : float):
        self.n1 = n1
        self.n2 = n2
        self.cost = cost

    def __str__(self) -> str:
        return 'Edge('+self.n1+','+self.n2+','+str(self.cost)+')'

class Graph:
    def __init__(self, edges : list[Edge] = []):
        self.edges : list[Edge] = edges
        self.nodes : list[str] = self._get_nodes()
        self.is_empty : bool = edges == []

    def create_graph_from_df(self, df : pd.DataFrame):
        self.edges = []
        for _, row in df.iterrows():
            edge = Edge(row['N1'], row['N2'], row['Cost'])
            self.edges.append(edge)
        self.nodes = self._get_nodes()
        self.is_empty : bool = self.edges == []

    def __str__(self) -> str:
        to_return = 'Graph(\n'
        for edge in self.edges:
            to_return += '    '+ str(edge) + '\n'
        to_return += ')'
        return to_return

    def _get_nodes(self) -> list[str]:
        nodes : list[str] = []
        for edge in self.edges:
            if edge.n1 not in nodes:
                nodes.append(edge.n1)
            if edge.n2 not in nodes:
                nodes.append(edge.n2)
        return nodes
    
    def get_cost(self, n1 : str, n2 : str):
        for edge in self.edges:
            if (edge.n1 == n1 and edge.n2 == n2) or (edge.n1 == n2 and edge.n2 == n1):
                return edge.cost
        return None

    def get_immediate_neighbor_nodes(self, node : str):
        immediate_neighbors = []
        for edge in self.edges:
            if edge.n1 == node:
                immediate_neighbors.append(edge.n2)
            elif edge.n2 == node:
                immediate_neighbors.append(edge.n1)
        return immediate_neighbors

    def to_dict(self) -> dict:
        graph = {}
        for edge in self.edges:
            if edge.n1 not in graph:
                graph[edge.n1] = {}
            if edge.n2 not in graph:
                graph[edge.n2] = {}
            graph[edge.n1][edge.n2] = edge.cost
            graph[edge.n2][edge.n1] = edge.cost
        return graph

    def get_shortest_path_DV(self, start_node: str, end_node: str):
        # Initialize distance vector for each node
        distance_vectors: dict[str, dict[str, float]] = {}
        for node in self.nodes:
            distance_vectors[node] = {}
            for neighbor in self.nodes:
                if node == neighbor:
                    distance_vectors[node][neighbor] = 0
                else:
                    distance_vectors[node][neighbor] = float('inf')

        # Set distance vector for edges in the graph
        for edge in self.edges:
            distance_vectors[edge.n1][edge.n2] = edge.cost
            distance_vectors[edge.n2][edge.n1] = edge.cost

        # Apply distance vector graph algorithm
        for k in self.nodes:
            for i in self.nodes:
                for j in self.nodes:
                    if distance_vectors[i][j] > distance_vectors[i][k] + distance_vectors[k][j]:
                        distance_vectors[i][j] = distance_vectors[i][k] + distance_vectors[k][j]

        # Extract shortest path from distance vectors
        shortest_path = [start_node]
        current_node = start_node

        while current_node != end_node:
            # Get the immediate neighbors of the current node
            immediate_neighbors = self.get_immediate_neighbor_nodes(current_node)
            cost_of_end_node_from_immediate_neighbors = {n : distance_vectors[n][end_node] for n in immediate_neighbors}

            # Find next node
            potential_new_current_node = current_node
            for n in immediate_neighbors:

                # If at the end node, check if it's the final hop
                if n == end_node:
                    if distance_vectors[current_node][n] == self.get_cost(current_node, n):
                        potential_new_current_node = n 

                # Otherwise, hop to the node with the least cost
                elif cost_of_end_node_from_immediate_neighbors[n] + distance_vectors[current_node][n] <= distance_vectors[current_node][end_node]:
                    potential_new_current_node = n

            # Update the current node
            current_node = potential_new_current_node

            # Update shortest path
            shortest_path.append(current_node)

            # In case of infinite loop
            if len(shortest_path) > len(self.nodes): break

        # Get total cost from distance vector
        total_cost = distance_vectors[start_node][end_node]

        # Convert distance vector table to pandas DataFrame
        dv = pd.DataFrame.from_dict(distance_vectors, orient='index')

        dv = dv.apply(lambda x: pd.Series(x))

        return total_cost, shortest_path, dv