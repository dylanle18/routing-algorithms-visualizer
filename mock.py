# TODO: Make a file similar to this one that handles Q1 and Q2 respectively
def mock(edges: list)-> list:
    return [
        {'node1': 'A', 'node2': 'B', 'isPath': 0, 'cost': 100},
        {'node1': 'A', 'node2': 'C', 'isPath': 1, 'cost': 200},
        {'node1': 'B', 'node2': 'C', 'isPath': 0, 'cost': 300},
        {'node1': 'B', 'node2': 'D', 'isPath': 0, 'cost': 400},
        {'node1': 'C', 'node2': 'D', 'isPath': 0, 'cost': 500},
        {'node1': 'C', 'node2': 'D', 'isPath': 0, 'cost': 600},
        {'node1': 'C', 'node2': 'F', 'isPath': 1, 'cost': 700},
        {'node1': 'E', 'node2': 'F', 'isPath': 2, 'cost': 800}
    ]
