##############################################################################
##########################   GRAPH ESTABLISHING   ############################
##############################################################################

import networkx as nx
adj_lanelet_dict = dict()
G = nx.DiGraph()

##############################################################################
########  CreateEdgeList(point_list): return edges of main graph G  ##########
##############################################################################
def CreateEdgeList( p):
    c = []
    prev = None
    for i in p:
        if prev != None:
            c.append([int(prev),int(i)])
        prev = i
    return c

##############################################################################
##  CreateEdgesBtwnLanelets(l, adj_dict): : return edges of lanelet graph L  #
##############################################################################
#return an array that include edges list between given lanelet  and its predessor and successor
def CreateEdgesBtwnLanelets(l):
    # we can manage previously added edges in here but it can be time waste. 
    #I am Not sure which is more efficient
    # Melike
    #TODO: add adjacency lanelets
    e = []
    a = []
    key = FindKeyGraphId(l.lanelet_id)
    if l.predecessor:
        for p in l.predecessor:
            predessor_key = FindKeyGraphId(p)
            e.append([predessor_key, key ])        
    if l.successor:
        for s in l.successor:
            successor_key = FindKeyGraphId(s)
            e.append([key, successor_key])     
    if l.adj_left_same_direction:
        a.append(l.adj_left)
    if l.adj_right_same_direction:
        a.append(l.adj_right)
    return e, a

##############################################################################
####  CreateLaneletGraph(lanelets): return a Graph conssit of Lanelets  ######
##############################################################################
def CreateLaneletGraph(lanelets):
    import networkx as nx
    import numpy as np
    #L:       is a directed graph for each of the lanelet
    #G:       is exist of graphs of lanelets and G mapped with lanelets' id
    #points:  for represent the each point in a lanelet
    #edges:   edges for each lanelet
    #adj_lanelet_dict:  it is for merging adj lanelets and their adj lanelets
    global G
    Graph_G = nx.DiGraph()
    global adj_lanelet_dict
    for lanelet in lanelets:
        i = lanelet.lanelet_id
        if not adj_lanelet_dict:
            graph_key = i
        else:
            graph_key = FindKeyGraphId(i)
        
        # if graph_key == i then we need to create a new lanelet graph else we create "bounded lanelets"
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
            distance =  lanelet.distance[-1] #total distance of a lanelet
            edgesLanelet, adjacent_lanelets = CreateEdgesBtwnLanelets(lanelet)
            Graph_G.add_node(graph_key, adj_lanelet = adjacent_lanelets , weight = distance, graph = L)  
            adj_lanelet_dict[graph_key] = adjacent_lanelets
        else:
            for l in adjacent_lanelets:
                if l not in adj_lanelet_dict[graph_key]:
                    adj_lanelet_dict[graph_key].append(l)
        #G add edges
        Graph_G.add_edges_from(edgesLanelet)
        G = Graph_G
    return G

##############################################################################
######  FindKeyGraphId(search_value, adj_dict): return key value for G   #####
######  It is necessary for finding "bounded lanelets" graph id          #####
##############################################################################
def FindKeyGraphId(search_value):
    global adj_lanelet_dict
    adj_dict = adj_lanelet_dict
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
##############################################################################
####################  FUNCTIONS IN THE PAPER  ################################
##############################################################################

##############################################################################
#########  V(obstacle, graph): return initial_lanelet, initial_node ##########
##############################################################################
def V(obstacle):
    import math
    
    points = []
    minDistances = []
    key_lanelets = []
    global G
    
    for l in obstacle.initial_center_lanelet_ids:
        key_lanelets.append(FindKeyGraphId(l))
    ## iterate initial lanelets of the obstacle
    # Question: In which situation there can be more than one itinial lanelet for a vehicle
    # Answer: the vehicles are examined with its occupancy (length, width and orientation considered)
    #in this case a vehicle might occupy more than one lanelet
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

##############################################################################
############  R(v(c)): return reachable vertecies by an obstacle ############
##############################################################################
from networkx import dfs_successors
def R(vc):
    global G
    key_vc = FindKeyGraphId(vc)
    reachable_vertices = dfs_successors(G, key_vc)
    if not reachable_vertices:
        reachable_vertices = {key_vc: []}
        
    return reachable_vertices

##############################################################################
############ M(v(c0), v(c1)) = R(v(c0)) n R (v(c1)): return Vm  ##############
##############################################################################
def M( v1, v2): 
    r1, r2 = dict(), dict()
    r1 = R(v1)
    r2 = R(v2)
    for key in r1.keys():
        if key in r2.keys():
            return key
        for values in r2.values():
            if key in values:
                return key
    
    for values in r1.values():
        for value in values:
            if value in r2.keys():
                return value
            for values2 in r2.values():
                if value in values2:
                    return value
                
    return None

##############################################################################
##########  Ps(v(c1), vm ): return  shortest path from v(c1) to vm ###########
##############################################################################
def P(v, vm):
    import networkx as nx
    shortest_path = None
    if vm is not None:
        shortest_path = nx.shortest_path(G, source = v, target = vm, weight = 'weight')
    return shortest_path

##############################################################################
##########  D(P1, P2): returns the maximum distance for P1 and P2  ###########
##############################################################################
def D(c1, c2):
    import math
    
    v1, n1 = V(c1)
    v2, n2 = V(c2)
    vm = M(v1, v2)

    #v1, v2, vm
    p1 = P(v1, vm)
    p2 = P(v2, vm)
    
    if p1 is None or p2 is None:
        return math.inf
    
    # measure distance considering nodes of the lanelets
    distance_p1 = 0
    distance_p2 = 0
    for lanelet in p1:
        key_lanelet = FindKeyGraphId(lanelet)
        distance_p1 = distance_p1 + (G.nodes[key_lanelet]['weight'])
        last_node_distance1 = (G.nodes[key_lanelet]['weight'])
    for lanelet in p2:
        key_lanelet = FindKeyGraphId(lanelet)
        distance_p2 = distance_p2 + (G.nodes[key_lanelet]['weight'])
        last_node_distance2 = (G.nodes[key_lanelet]['weight'])
        
    #subtrack distances untill vehicles current node
    distance_p1 = distance_p1 - (G.nodes[v1]['graph'].nodes[n1]['distance']) - last_node_distance1
    distance_p2 = distance_p2 - (G.nodes[v2]['graph'].nodes[n2]['distance']) - last_node_distance2
    
    distance = max(distance_p1, distance_p2,0)
    #TODO decide calculate real distance or calculate just lanelet lentgh is enaugh
    return distance