##########   GRAPH   ##########
#there have to be a quick way instead of using a for loop
#creating edges between nodes in a lanelet
##########   GRAPH   ##########
#there have to be a quick way instead of using a for loop
#creating edges between nodes in a lanelet

import networkx as nx
adj_lanelet_dict = dict()
G = nx.DiGraph()

def CreateEdgeList( p):
    c = []
    prev = None
    for i in p:
        if prev != None:
            c.append([int(prev),int(i)])
        prev = i
    return c

#return an array that include edges list between given lanelet  and its predessor and successor
def CreateEdgesBtwnLanelets(l, adj_dict):
    # we can manage previously added edges in here but it can be time waste. 
    #I am Not sure which is more efficient
    # Melike
    #TODO: add adjacency lanelets
    e = []
    a = []
    key = FindKeyGraphId(l.lanelet_id, adj_dict)
    if l.predecessor:
        for p in l.predecessor:
            predessor_key = FindKeyGraphId(p, adj_dict)
            e.append([predessor_key, key ])        
    if l.successor:
        for s in l.successor:
            successor_key = FindKeyGraphId(s,adj_dict)
            e.append([key, successor_key])     
    if l.adj_left_same_direction:
        a.append(l.adj_left)
    if l.adj_right_same_direction:
        a.append(l.adj_right)
    return e, a

def CreateLaneletGraph(lanelets):
    import networkx as nx
    import numpy as np
    #L:       is a directed graph for each of the lanelet
    #G:       is exist of graphs of lanelets and G mapped with lanelets' id
    #points:  for represent the each point in a lanelet
    #edges:   edges for each lanelet
    #adj_lanelet_dict:  it is for merging adj lanelets and their adj lanelets
    global adj_lanelet_dict
    global G
    
    for lanelet in lanelets:
        i = lanelet.lanelet_id
        if not adj_lanelet_dict:
            graph_key = i
        else:
            graph_key = FindKeyGraphId(i, adj_lanelet_dict)
        
        # if graph_key == i then we need to create a new lanelet graph
        if graph_key == i: 
            ## Establish L
            L = nx.DiGraph()
            #L add nodes and edges
            points = np.array(range(0,(len(lanelet.distance))))
            edges = CreateEdgeList(points)
            ### set each node in Lanelet one by one with its vertex and distance
            for k in range(len(points)):
                L.add_node(points[k], distance = lanelet.distance[k], vertices=lanelet.center_vertices[k])
            ###
            L.add_edges_from(edges)

            #G add nodes
            # adding the graph of lanelet with id i and adjecent lanelet adj_lanelet
            edgesLanelet, adjacent_lanelets = CreateEdgesBtwnLanelets(lanelet, adj_lanelet_dict)
            G.add_node(graph_key, adj_lanelet = adjacent_lanelets , graph = L)  
            adj_lanelet_dict[graph_key] = adjacent_lanelets
        else:
            for l in adjacent_lanelets:
                if l not in adj_lanelet_dict[graph_key]:
                    adj_lanelet_dict[graph_key] += l
        #G add edges
        G.add_edges_from(edgesLanelet)
        adj_lanelet_dict = adj_lanelet_dict
    return G

def FindKeyGraphId(search_value, adj_dict):
    values = list(adj_dict.values())
    keys = list(adj_dict.keys())
    key = None

    for v in values:
        if search_value in v:
            index = values.index(v)
            key = keys[index]
    if key is None:
        key = search_value

    return key


##############################################################################################
########## Vertex  v(obstacle, graph): return initial_lanelet, initial_node ##################
##############################################################################################
def V(obstacle):
    import math
    
    points = []
    minDistances = []
    key_lanelets = []
    global adj_lanelet_dict
    global G
    # selftest =  {53: [], 54: [55], 56: [], 57: [58], 59: [], 60: [61], 62: [], 63: [68], 64: [66], 65: [], 67: []}
    for l in obstacle.initial_center_lanelet_ids:
        key_lanelets.append(FindKeyGraphId(l,adj_lanelet_dict))
    ## iterate initial lanelets of the obstacle
    # Question: In which situation there can be more than one itinial lanelet for a vehicle
    for l in key_lanelets:
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
    return list(key_lanelets)[index], points[index]

################################################################
##########  R(v(c)) reachable vertecies by a pbstacle ##########
################################################################
from networkx import dfs_successors
def R(vc):
    global G
    reachable_vertices = dfs_successors(G, vc)
    return reachable_vertices



############################################################
########## M(v(c0), v(c1)) = R(v(c0)) n R (v(c1)) ##########
############################################################
def M( v1, v2): 
    r1, r2 = dict(), dict()
    r1 = R(v1)
    r2 = R(v2)
    common_vertices = []

    for key in r1.keys():
        for k in r2.keys():
            if k == key or k == r1[key][0]:
                common_vertices.append(k)
            if r2[k][0] == key or r2[k][0] == r1[key][0]:
                common_vertices.append(r2[k][0])

    common_vertices = list(set(common_vertices)) # make unique the list
    return common_vertices