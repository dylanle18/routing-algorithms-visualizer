import streamlit as st
import graphviz as gv
import pandas as pd
from utils import Edge, Graph
import dijkstra as dj

def render_settings(graph : Graph):
    st.title('Visualizer Settings:')

    # get nodes for selection
    nodes = graph.nodes

    if graph.is_empty:
        st.warning("Empty Graph")
        return None,None,None,None

    # select start and end nodes
    start = st.selectbox("Select start node :red_circle:", ['Select Node']+nodes, 0)
    end = st.selectbox("Select end node :large_blue_circle:", ['Select Node']+nodes, 0)

    # check if start and end are not the same
    if start == end and start != 'Select Node':
        st.warning("Please select different start and end nodes")
        return None,None,None,None

    s = None
    e = None

    if start != 'Select Node':
        s = start

    if end != 'Select Node':
        e = end

    algo = st.selectbox("Select Algorithm to run", ["Select Algorithm", "Dijkstra's", "DVR"], 0)
    if algo == "Select Algorithm":
        return None, None, s, e

    if algo == 'DVR':
        cost, path = graph.get_shortest_path_DV(start_node=start[0], end_node=end[0])

    if algo == "Dijkstra's":
        # TODO: use Dijkstra
        cost, path, distTo, edgeTo = dj.get_shortest_path_DJ(graph.to_dict(), start[0], end[0])
        print(start, end)

    return cost, path, s, e



def render_customization():
    default_graph = {
        'N1' : ['A','A','B','B','C','C','E'],
        'N2' : ['B','C','C','D','D','F','F'],
        'Cost' : [100.0,200.0,300.0,400.0,600.0,700.0,800.0]
    }

    st.subheader('Set Graph Values')

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button('Set Graph to Default Example'):
            graph_values = pd.DataFrame(default_graph)

    graph_values = pd.DataFrame(default_graph)

    with col2:
        if st.button('Reset Graph'):
            graph_values = pd.DataFrame({
                'N1' : pd.Series(dtype='str'),
                'N2' : pd.Series(dtype='str'),
                'Cost' : pd.Series(dtype='float')
            })

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

cost, path_list, s_node, e_node = None, None, None, None

if graph.is_empty:
    st.warning("Your Graph is empty. Please fill it first")

with st.sidebar:
    cost, path_list, s_node, e_node = render_settings(graph)

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
if 'step_number' in st.session_state:
    if path_list:
        step_number = min(st.session_state['step_number'], len(path_list))
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
        step_number = min(step_number+1, len(path_list))
with col3:
    if path_list:
        st.write(f'Step {step_number-1}')
    else:
        st.write('Step ...')
st.session_state['step_number'] = step_number



# Generate path digraph
path = {}
if path_list:
    for i in range(len(path_list[:step_number])-1):
        path[path_list[i]] = path_list[i+1]



# Render graph
if not graph.is_empty:
    graph_visual.attr('node', color='gray')
    graph_visual.attr('node', shape='oval')
    for edge in graph.edges:
        if edge.n1 in path and path[edge.n1] == edge.n2:
            graph_visual.edge(edge.n1, edge.n2, label=str(edge.cost), dir='forward', color='darkseagreen4', penwidth='2', arrowsize='1.5')
        elif edge.n2 in path and path[edge.n2] == edge.n1:
            graph_visual.edge(edge.n1, edge.n2, label=str(edge.cost), dir='back', color='darkseagreen4', penwidth='2', arrowsize='1.5')
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
