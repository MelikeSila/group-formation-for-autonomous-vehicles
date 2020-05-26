# return initial vertex of the given obstacle ( v(c0)):
# return x and y coordinates as numpy array [x, y]
def v( obs):
    return obs.initial_state.position

"""
Sample using of v( obs):

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
    e = []
    if l.predecessor:
        for p in l.predecessor:
            e.append([p, l.lanelet_id ])        
    if l.successor:
        for s in l.successor:
            e.append([l.lanelet_id, s])        
    return e

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
        edgesLanelet = CreateEdgesBtwnLanelets(lanelet)
        G.add_node(i, graph = L)  # add to G the graph of lanelet with id i
        G.add_edges_from(edgesLanelet)
    return G

"""
Sample Using of CreateLaneletGraph(lanelets):

#distance
#adj_left=None, adj_left_same_direction=None, adj_right=None, ad_right_same_direction=None, 
#predecessor, succesor
#line_marking_right_vertices
options2 = {
    'node_color': 'green',
    'node_size': 1500,
    'width': 1,
}

import networkx as nx
lanelets = scenario.lanelet_network.lanelets
G = CreateLaneletGraph(lanelets)
plt.subplot(121)
nx.draw(G.nodes[50195]['graph'], with_labels=True, font_weight='bold') #for reaching the graph of lanelet with id i
plt.subplot(122)
nx.draw
nx.draw_circular(G,with_labels=True, font_weight='bold', **options2)
plt.show()
"""