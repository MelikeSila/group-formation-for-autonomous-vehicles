##########   GRAPH   ##########
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
    import numpy as np
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
        points = np.array(range(0,(len(lanelet.distance))))
        edges = CreateEdgeList(points)
        ### set each node in Lanelet one by one with its vertex and distance
        for k in range(len(points)):
            L.add_node(points[k], distance = lanelet.distance[k], vertices=lanelet.center_vertices[k])
        ###
        L.add_edges_from(edges)
        #G add nodes and edges
        edgesLanelet, adjacent_lanelets = CreateEdgesBtwnLanelets(lanelet)
        G.add_node(i, adj_lanelet = adjacent_lanelets , graph = L)  # adding the graph of lanelet with id i and adjecent lanelet adj_lanelet
        G.add_edges_from(edgesLanelet)
    return G

########## Vertex  v(obstacle, graph): return initial_lanelet, initial_node ###################
### the function for finding initial lanelet and its initial vertex of an obstacle and.
###############################################################################################
def v(obstacle, G):
    import math
    points = []
    minDistances = []
    ## iterate initial lanelets of the obstacle
    # Question: In which situation there can be more than one itinial lanelet for a vehicle
    for l in obstacle.initial_center_lanelet_ids:
        distances = []
        # iterate all nodes in a lanelet
        for i in range(len(G.nodes[l]['graph'].nodes)):
            #get the initial x and y of the vehicle
            xv = obstacle.initial_state.position[0]
            yv = obstacle.initial_state.position[1]
            #get the x and y of the lanelet's node
            xn = G.nodes[l]['graph'].nodes[i]['vertices'][0]
            yn = G.nodes[l]['graph'].nodes[i]['vertices'][1]
            ## calculate distance between the vehicle and a node
            distances.append(math.sqrt( ( xv - xn )**2 + ( yv - yn )**2 ))
        # get index of the nearest node to the vehicle and collect the minumum distances of lanelets
        minDistances.append(min(distances))
        points.append(distances.index(min(distances)))
    index = (minDistances.index(min(minDistances)))
    return list(obstacle.initial_center_lanelet_ids)[index], points[index]