# return initial vertex of the given obstacle ( v(c0)):
# return x and y coordinates as numpy array [x, y]
def v( obs):
    return obs.initial_state.position

"""
Sample using:
obstacles = scenario.obstacles
for o in obstacles:
    x, y = v(o)
    print(x)
    print(y)
"""
def CreateLaneletGraph(lanelets):
    import networkx as nx
    import matplotlib.pyplot as plt
    #L is a directed graph for each of the lanelet.
    #G is exist of graphs of lanelets and G mapped with lanelets' id
    G = nx.DiGraph()
    for lanelet in lanelets:
        i = lanelet.lanelet_id
        L = nx.DiGraph()
        L.add_nodes_from([1,2])
        L.add_edges_from([(3, 4), (4, 5)])
        G.add_node(i, graph = L)  # add to G the graph of lanelet with id i
    return G

"""
Sample Using:

#distance
#adj_left=None, adj_left_same_direction=None, adj_right=None, ad_right_same_direction=None, 
#predecessor, succesor
#line_marking_right_vertices
import networkx as nx
lanelets = scenario.lanelet_network.lanelets
G = CreateLaneletGraph(lanelets)
plt.subplot(121)
nx.draw(G.nodes[1]['graph'], with_labels=True, font_weight='bold') #for reaching the graph of lanelet with id i
plt.subplot(122)
nx.draw(G,with_labels=True, font_weight='bold')
plt.show()
"""