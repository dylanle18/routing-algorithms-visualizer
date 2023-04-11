import streamlit as st
import graphviz as gv
import pandas as pd
from utils import Edge, Graph
import dijkstra as dj

def render_settings(graph : Graph):
    st.title('Visualizer Settings:')

    # get nodes for selection
    nodes = graph.nodes
    nodes.sort()

    if graph.is_empty:
        st.warning("Empty Graph")
        return None,None,None,None,None,None,None

    # select start and end nodes
    start = st.selectbox("Select start node :red_circle:", ['Select Node']+nodes, 0)
    end = st.selectbox("Select end node :large_blue_circle:", ['Select Node']+nodes, 0)

    # check if start and end are not the same
    if start == end and start != 'Select Node':
        st.warning("Please select different start and end nodes")
        return None,None,None,None,None,None,None

    s = None
    e = None

    if start != 'Select Node':
        s = start

    if end != 'Select Node':
        e = end

    if start == 'Select Node' and end == 'Select Node':
        return None,None,None,None,None,None,None
    elif start == 'Select Node':
        return None,None,None,e,None,None,None
    elif end == 'Select Node':
        return None,None,s,None,None,None,None

    algo = st.selectbox("Select Algorithm to run", ["Select Algorithm", "Dijkstra's", "DVR"], 0)
    if algo == "Select Algorithm":
        return None, None, s, e, None, None, None

    cost = 0
    path = []
    table = None
    history = []

    if algo == 'DVR' and s and e:
        cost, path, table, history = graph.get_shortest_path_DV(start_node=s, end_node=e)

    elif algo == "Dijkstra's":
        cost, path, distTo, edgeTo, history = dj.get_shortest_path_DJ(graph.to_dict(), start[0], end[0])

        dataFrame1 = pd.DataFrame(list(distTo.items()), columns=['Letter', 'DistTo'])
        dataFrame2 = pd.DataFrame(list(edgeTo.items()), columns=['Letter', 'EdgeTo'])

        table = pd.merge(dataFrame1, dataFrame2, on='Letter', how='outer').set_index('Letter')
    else:
        algo = None

    return cost, path, s, e, table, algo, history



def render_customization():
    default_graph = {
        'N1' : ['A','A','B','B','C','C','E'],
        'N2' : ['B','C','C','D','D','F','F'],
        'Cost' : [100.0,200.0,300.0,400.0,600.0,700.0,800.0]
    }

    st.subheader('Set Graph Values')

    # col1, col2 = st.columns([1, 5])

    graph_values = pd.DataFrame(default_graph)

    graph_values = graph_values.reset_index(drop=True)
    graph_values = st.experimental_data_editor(graph_values, num_rows="dynamic", use_container_width=True)

    graph_values = graph_values.replace('', float('NaN'))
    graph_values.dropna(how='any', inplace=True)

    st.text("Note that you can delete a row by selecting it and pressing 'DELETE'")

    return graph_values



# Main app
st.title('Routing Algorithms Visualizer')

graph_values = render_customization()

graph = Graph()
graph.create_graph_from_df(graph_values)

cost, path_list, s_node, e_node, table, algo, history = None, None, None, None, None, None, None

with st.sidebar:
    cost, path_list, s_node, e_node, table, algo, history = render_settings(graph)

if graph.is_empty:
    st.warning("Your Graph is empty. Please fill it first")
    exit()



# Graph Nodes
graph_visual = gv.Graph()
graph_visual.attr(rankdir='LR')

graph_visual.attr('node', width='.7', height='.7', style='filled')

if s_node:
    graph_visual.attr('node', color='darksalmon')
    graph_visual.node(s_node)

if e_node:
    graph_visual.attr('node', color='lightblue')
    graph_visual.node(e_node)

st.subheader('The Resultant Graph')



# Back and Next Buttons
st.text('Press Back and Next to go through the path')
stepTable = 0
stepPath = 0
stepMax = 0
if 'step_number' in st.session_state:
    if path_list:
        stepTable = len(history)
        stepPath = len(path_list)
        stepMax = stepTable + stepPath - 1
        step_number = min(st.session_state['step_number'], stepMax)
    else:
        step_number = st.session_state['step_number']
else:
    step_number = 1
col1, col2, col3 = st.columns([.5,.5, 3])
with col1:
    if st.button('Back', disabled=not path_list):
        step_number = max(step_number-1, 1)
with col2:
    if st.button('Next', disabled=not path_list):
        step_number = min(step_number+1, stepMax)
with col3:
    if path_list:
        st.write(f'Step {step_number-1}')
    else:
        st.write('Step ...')
st.session_state['step_number'] = step_number



# Generate path digraph
path = {}
if path_list and step_number > stepTable:
    for i in range(len(path_list[:step_number - stepTable + 1])-1):
        path[path_list[i]] = path_list[i+1]



# Render graph
graph_visual.attr('node', color='gray')
graph_visual.attr('node', shape='oval')

color = 'darkorange3' if algo == "Dijkstra's" else 'darkseagreen4'

for edge in graph.edges:
    if step_number > stepTable and edge.n1 in path and path[edge.n1] == edge.n2:
        graph_visual.edge(edge.n1, edge.n2, label=str(edge.cost), dir='forward', color=color, penwidth='2', arrowsize='1.5')
    elif step_number > stepTable and edge.n2 in path and path[edge.n2] == edge.n1:
        graph_visual.edge(edge.n1, edge.n2, label=str(edge.cost), dir='back', color=color, penwidth='2', arrowsize='1.5')
    else:
        graph_visual.edge(edge.n1, edge.n2, label=str(edge.cost))
st.graphviz_chart(graph_visual)



# Render cost and path
if path_list:
    st.write(f'Cost is `{cost}`'.format(cost))
    path_list_str = '['
    for p in path_list:
        path_list_str += p+'->'
    path_list_str = path_list_str[:-2]
    path_list_str += ']'
    st.write(f'Path is `{path_list_str}`'.format(path_list_str))


if type(table) == pd.DataFrame:
    if step_number <= stepTable:
        st.write(history[step_number - 1])
    else:
        st.write(history[stepTable - 1])
