# return initial vertex of the given obstacle ( v(c0)):
# return x and y coordinates as numpy array [x, y]
def v( obs):
    return obs.initial_state.position

"""
Sample usage of v( obs):

obstacles = scenario.obstacles
for o in obstacles:
    x, y = v(o)
    print(x)
    print(y)
"""
                ####   GRAPH   ####
#there have to be a quick way instead of using a for loop
#creating edges between nodes in a lanelet
def CreateEdgeList(p):
    c = []
    prev = None
    for i in p:
        if prev != None:
            c.append([int(prev),int(i)])
        prev = i
    return c

#return an array that include edges list between given lanelet  and its predessor and successor
def CreateEdgesBtwnLanelets(l):
    # we can manage previously added edges in here but it can be time waste. 
    #I am Not sure which is more efficient
    # Melike
    #TODO: add adjacency lanelets
    e = []
    a = []
    if l.predecessor:
        for p in l.predecessor:
            e.append([p, l.lanelet_id ])        
    if l.successor:
        for s in l.successor:
            e.append([l.lanelet_id, s])     
    if l.adj_left_same_direction:
        a.append(l.adj_left)
        #e.append(l.lanelet_id, l.adj_left.lanelet_id) #TODO decide do we need to connect adj lanelets
        #e.append(l.adj_left.lanelet_id, l.lanelet_id)
    if l.adj_right_same_direction:
        a.append(l.adj_right)
        #e.append(l.lanelet_id, l.adj_right.lanelet_id)
        #e.append(l.adj_right.lanelet_id, l.lanelet_id)
    return e, a

def CreateLaneletGraph(lanelets):
    import networkx as nx
    import matplotlib.pyplot as plt
    #L:       is a directed graph for each of the lanelet
    #G:       is exist of graphs of lanelets and G mapped with lanelets' id
    #points:  for represent the each point in a lanelet
    #edges:   edges for each lanelet
    #
    G = nx.DiGraph()
    for lanelet in lanelets:
        i = lanelet.lanelet_id
        L = nx.DiGraph()
        #L add nodes and edges
        points = list(range(1,len(lanelet.distance)))
        edges = CreateEdgeList(points)
        L.add_nodes_from(points, distance = lanelet.distance, vertices=lanelet.center_vertices)
        L.add_edges_from(edges)
        #G add nodes and edges
        edgesLanelet, adjacent_lanelets = CreateEdgesBtwnLanelets(lanelet)
        G.add_node(i, adj_lanelet = adjacent_lanelets , graph = L) #adding lanelet graph with id and adjecent lanelet
        G.add_edges_from(edgesLanelet)
    return G

"""
######## Sample Usage ############
## First run here for testing
## It include scenario and brief 
## drawing
##################################

import os
import matplotlib.pyplot as plt
from IPython import display

# import functions to read xml file and visualize commonroad objects
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.draw_dispatch_cr import draw_object

# generate path of the file to be opened
#file_path = "ZAM_Tutorial-1_1_T-1.xml"
#file_path = "ZAM_Tjunction-1_66_T-1.xml"
file_path = "CHN_Cho-2_1_T-1.xml"

# read in the scenario and planning problem set
crf = CommonRoadFileReader(file_path)
scenario, planning_problem_set = crf.open()

# plot the scenario for 40 time step, here each time step corresponds to 0.1 second
for i in range(0, 40):
    # uncomment to clear previous graph
    display.clear_output(wait=True)
    
    plt.figure(figsize=(20, 10))
    # plot the scenario at different time step
    draw_object(scenario, draw_params={'time_begin': i})
    # plot the planning problem set
    draw_object(planning_problem_set)
    plt.gca().set_aspect('equal')
    plt.show()
"""




"""
########## Sample Usage ###########
Sample Usage of CreateLaneletGraph(lanelets):

#distance
# lanelet_id
#adj_left=None, adj_left_same_direction=None, adj_right=None, ad_right_same_direction=None, 
#predecessor, succesor
#line_marking_right_vertices

options1 = {
    'node_color': 'lightgreen',
    'node_size': 500,
    'width': 1,
}
options2 = {
    'node_color': 'green',
    'node_size': 500,
    'width': 1,
}

import networkx as nx
lanelets = scenario.lanelet_network.lanelets
G = CreateLaneletGraph(lanelets)
plt.subplot(121)
nx.draw_circular(G.nodes[lanelets[0].lanelet_id]['graph'], with_labels=True, font_weight='bold', **options1) #for reaching the graph of lanelet with id i
plt.subplot(122)
nx.draw_circular(G,with_labels=True, font_weight='bold', **options2)
plt.show()
"""
"""

########## Sample Usage ###########
See more clear graphs and data

print(G.nodes)
plt.rcParams['figure.figsize'] = (10.0, 10.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
nx.draw(G,with_labels=True, font_weight='bold', **options2)
plt.show()
i = 1
for lanelet in lanelets:
    print(lanelet)
    plt.subplot(1, len(lanelets), i)
    nx.draw(G.nodes[lanelet.lanelet_id]['graph'], with_labels=True, font_weight='bold', **options1) #for reaching the graph of lanelet with id i
    print(lanelet.adj_left_same_direction, ": ", lanelet.adj_left)
    print(lanelet.adj_right_same_direction, ": ", lanelet.adj_right)
    #if 53 in G.nodes[lanelet.lanelet_id]['adj_lanelet']: #adjacent lanelet control # contain()
    #    print(True)
    i = i+1
plt.show()
"""