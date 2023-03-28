import streamlit as st
import graphviz as gv

# TODO: Import final functions here
from mock import mock

st.title('Routing Algorithms Visualizer')

# edges init
edges = [
    {'node1': 'A', 'node2': 'B', 'isPath': 0, 'cost': 100},
    {'node1': 'A', 'node2': 'C', 'isPath': 0, 'cost': 200},
    {'node1': 'B', 'node2': 'C', 'isPath': 0, 'cost': 300},
    {'node1': 'B', 'node2': 'D', 'isPath': 0, 'cost': 400},
    {'node1': 'C', 'node2': 'D', 'isPath': 0, 'cost': 500},
    {'node1': 'C', 'node2': 'D', 'isPath': 0, 'cost': 600},
    {'node1': 'C', 'node2': 'F', 'isPath': 0, 'cost': 700},
    {'node1': 'E', 'node2': 'F', 'isPath': 0, 'cost': 800}
]

# get nodes for selection
nodes = []
for edge in edges:
    if edge['node1'] not in nodes:
        nodes.append(edge['node1'])
    if edge['node2'] not in nodes:
        nodes.append(edge['node2'])

# select start and end nodes
start = st.multiselect("Select start node", nodes, [], max_selections=1)
end = st.multiselect("Select end node", nodes, [], max_selections=1)

# check if start and end are not the same
if start == end:
    st.warning("Please select different start and end nodes")

# final render
elif start != [] and end != []:
    col1, col2 = st.columns(2)

    # TODO: use Dijkstra instead of mock
    edges = mock(edges)

    with col1:
        st.title("Q1: Dijkstra's")
        graph = gv.Graph()
        graph.attr('node', shape='square')
        graph.node(start[0])
        graph.node(end[0])
        graph.attr('node', shape='circle')

        for edge in edges:
            if edge['isPath'] > 0:
                dir = "forward" if edge['isPath'] == 1 else "back"
                graph.edge(edge['node1'], edge['node2'], label=str(
                    edge['cost']), color='red', dir=dir)
            else:
                graph.edge(edge['node1'], edge['node2'],
                           label=str(edge['cost']))

        st.graphviz_chart(graph, use_container_width=True)

    # TODO: use DV instead of mock
    edges = mock(edges)

    with col2:
        st.title("Q2: DV")
        graph = gv.Graph()
        graph.attr('node', shape='square')
        graph.node(start[0])
        graph.node(end[0])
        graph.attr('node', shape='circle')

        for edge in edges:
            if edge['isPath'] > 0:
                dir = "forward" if edge['isPath'] == 1 else "back"
                graph.edge(edge['node1'], edge['node2'], label=str(
                    edge['cost']), color='blue', dir=dir)
            else:
                graph.edge(edge['node1'], edge['node2'],
                           label=str(edge['cost']))

        st.graphviz_chart(graph, use_container_width=True)
