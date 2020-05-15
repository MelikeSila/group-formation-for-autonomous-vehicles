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
def CreateLaneletGraph(scenario):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    GraphDict = dict()
    lanelets = scenario.lanelet_network.lanelets
    for i in lanelets:
        prev = None
        for k in i.center_vertices:
            node = k[0]
            G.add_node(node)
            if prev:
                G.add_edge(prev,node)
            prev = node
        GraphDict[i.lanelet_id]= G
    return GraphDict

"""
Sample Using:

LaneletGraphDict = createLaneletGraph(scenario)
for i in GraphDict:
        print("******************************************")
        print(LaneletGraphDict[i])
        nx.draw(LaneletGraphDict[i], with_labels=True)
plt.show()
"""