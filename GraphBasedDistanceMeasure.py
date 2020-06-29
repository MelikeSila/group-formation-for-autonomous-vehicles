##############################################################################
##########################   GRAPH ESTABLISHING   ############################
##############################################################################
class ScenarioGraph:
    
    def __init__(self, scenario, planning_problem_set):
        self.scenario = scenario
        self.planning_problem_set = planning_problem_set
        self.obstacles = scenario.obstacles
        self.lanelets = scenario.lanelet_network.lanelets
        self.adj_lanelet_dict = dict()
        
        self.first_ego_vehicle_id = None
        self.ego_vehicle_ids = list()
        self.ego_vehicle_dic_list = self.__InitializeEgoVehicleAttributes()
        
        self.scenario_graph = self._CreateLaneletGraph()
    
    
    ##############################################################################
    ########  CreateEdgeList(point_list): return edges of main graph G  ##########
    ##############################################################################
    def __CreateEdgeList(self, p):
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
    def __CreateEdgesBtwnLanelets(self, l):
        # we can manage previously added edges in here but it can be time waste. 
        #I am Not sure which is more efficient
        # Melike
        #TODO: add adjacency lanelets
        e = []
        a = []
        key = self.__FindKeyGraphId(l.lanelet_id)
        if l.predecessor:
            for p in l.predecessor:
                predessor_key = self.__FindKeyGraphId(p)
                e.append([predessor_key, key ])        
        if l.successor:
            for s in l.successor:
                successor_key = self.__FindKeyGraphId(s)
                e.append([key, successor_key])     
        if l.adj_left_same_direction:
            a.append(l.adj_left)
        if l.adj_right_same_direction:
            a.append(l.adj_right)
        return e, a

    ##############################################################################
    ####  CreateLaneletGraph(lanelets): return a Graph conssit of Lanelets  ######
    ##############################################################################
    def _CreateLaneletGraph(self):
        import networkx as nx
        import numpy as np
        lanelets = self.lanelets
        #L:       is a directed graph for each of the lanelet
        #points:  for represent the each point in a lanelet
        #edges:   edges for each lanelet
        #adj_lanelet_dict:  it is for merging adj lanelets and their adj lanelets
        
        Graph_G = nx.DiGraph()
        adj_lanelet_dict = self.adj_lanelet_dict
        for lanelet in lanelets:
            i = lanelet.lanelet_id
            if not adj_lanelet_dict:
                graph_key = i
            else:
                graph_key = self.__FindKeyGraphId(i)

            # if graph_key == i then we need to create a new lanelet graph else we create "bounded lanelets"
            if graph_key == i: 
                ## Establish L
                L = nx.DiGraph()
                #L add nodes and edges
                points = np.array(range(0,(len(lanelet.distance))))
                edges = self.__CreateEdgeList(points)
                ### set each node in Lanelet one by one with its vertex and distance
                for k in range(len(points)):
                    L.add_node(points[k], distance = lanelet.distance[k], vertices=lanelet.center_vertices[k])
                ###
                L.add_edges_from(edges)

                #G add nodes
                # adding the graph of lanelet with id i and adjecent lanelet adj_lanelet
                distance =  lanelet.distance[-1] #total distance of a lanelet
                edgesLanelet, adjacent_lanelets = self.__CreateEdgesBtwnLanelets(lanelet)
                Graph_G.add_node(graph_key, adj_lanelet = adjacent_lanelets , weight = distance, graph = L)  
                adj_lanelet_dict[graph_key] = adjacent_lanelets
            else:
                for l in adjacent_lanelets:
                    if l not in adj_lanelet_dict[graph_key]:
                        adj_lanelet_dict[graph_key].append(l)
            self.adj_lanelet_dict = adj_lanelet_dict
            #G add edges
            Graph_G.add_edges_from(edgesLanelet)
            self.scenario_graph = Graph_G
        return self.scenario_graph

    ##############################################################################
    ######  FindKeyGraphId(search_value, adj_dict): return key value for G   #####
    ######  It is necessary for finding "bounded lanelets" graph id          #####
    ##############################################################################
    def __FindKeyGraphId(self, search_value):
        adj_lanelet_dict = self.adj_lanelet_dict
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
    def V(self, obstacle):
        import math

        points = []
        minDistances = []
        key_lanelets = []
        G = self.scenario_graph

        for l in obstacle.initial_center_lanelet_ids:
            key_lanelets.append(self.__FindKeyGraphId(l))
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
    def R(self, vc):
        from networkx import dfs_successors
        G = self.scenario_graph
        key_vc = self.__FindKeyGraphId(vc)
        reachable_vertices = dfs_successors(G, key_vc)
        if not reachable_vertices:
            reachable_vertices = {key_vc: []}

        return reachable_vertices

    ##############################################################################
    ############ M(v(c0), v(c1)) = R(v(c0)) n R (v(c1)): return Vm  ##############
    ##############################################################################
    def M(self, v1, v2): 
        r1, r2 = dict(), dict()
        r1 = self.R(v1)
        r2 = self.R(v2)
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
    def P(self, v, vm):
        import networkx as nx
        shortest_path = None
        if vm is not None:
            shortest_path = nx.shortest_path(self.scenario_graph, source = v, target = vm, weight = 'weight')
        return shortest_path

    ##############################################################################
    ##########  D(P1, P2): returns the maximum distance for P1 and P2  ###########
    ##############################################################################
    def D(self, c1, c2):
        import math
        G = self.scenario_graph
        v1, n1 = self.V(c1)
        v2, n2 = self.V(c2)
        vm = self.M(v1, v2)

        #v1, v2, vm
        p1 = self.P(v1, vm)
        p2 = self.P(v2, vm)

        if p1 is None or p2 is None:
            return math.inf

        # measure distance considering nodes of the lanelets
        distance_p1 = 0
        distance_p2 = 0
        for lanelet in p1:
            key_lanelet = self.__FindKeyGraphId(lanelet)
            distance_p1 = distance_p1 + (G.nodes[key_lanelet]['weight'])
            last_node_distance1 = (G.nodes[key_lanelet]['weight'])
        for lanelet in p2:
            key_lanelet = self.__FindKeyGraphId(lanelet)
            distance_p2 = distance_p2 + (G.nodes[key_lanelet]['weight'])
            last_node_distance2 = (G.nodes[key_lanelet]['weight'])

        #subtrack distances untill vehicles current node
        distance_p1 = distance_p1 - (G.nodes[v1]['graph'].nodes[n1]['distance']) - last_node_distance1
        distance_p2 = distance_p2 - (G.nodes[v2]['graph'].nodes[n2]['distance']) - last_node_distance2

        distance = max(distance_p1, distance_p2,0)
        #TODO decide calculate real distance or calculate just lanelet lentgh is enaugh
        return distance
    ##############################################################################
    ###########  GenerateNewEgoVehicleID(): generate a new unique ################
    ###########  id for ego vehicles in the problem set           ################
    ##############################################################################
    def __GenerateNewEgoVehicleID(self):
        #take current ids
        first_ego_vehicle_id = self.first_ego_vehicle_id
        ego_vehicle_ids = self.ego_vehicle_ids

        if first_ego_vehicle_id is None:
            #set first ego vehicle id if it is none and return the id
            first_ego_vehicle_id = -1
            #add the new id to list of the ego vehicle ids
            ego_vehicle_ids.append(first_ego_vehicle_id)
            #update constructor attributes
            self.first_ego_vehicle_id = first_ego_vehicle_id
            self.ego_vehicle_ids = ego_vehicle_ids
            
            return first_ego_vehicle_id
        
        #find a new unique id
        new_id = first_ego_vehicle_id
        while new_id in ego_vehicle_ids:
            new_id = new_id-1
        
        #add the new id to list of the ego vehicle ids
        ego_vehicle_ids.append(new_id)
        #update constructor attributes
        self.first_ego_vehicle_id = first_ego_vehicle_id
        self.ego_vehicle_ids = ego_vehicle_ids
        
        return new_id
    
    #####  LANELET ID OF EGO VEHICLE  #####
    #find lanelet id list for ego_vehicles in the problem statements set
    def __InitializeEgoVehicleAttributes(self):
        from commonroad.scenario.lanelet import LaneletNetwork

        planning_problem_set = self.planning_problem_set
        ego_vehicle_dic_list = list()
        ego_vehicle_dic = dict()

        for pp_key in planning_problem_set.planning_problem_dict:
            
            initial_position = list()
            #get initial_positions of the ego vehicle
            pp = planning_problem_set.planning_problem_dict[pp_key]
            initial_position.append(pp.initial_state.position)
            ego_vehicle_id = self.__GenerateNewEgoVehicleID()
            ego_vehicle_lanelet_ids = LaneletNetwork.find_lanelet_by_position( self.scenario.lanelet_network, 
                                                                              point_list = list(initial_position ))

            #set the ego vehicle initial state to ego_vehicle_dic
            ego_vehicle_dic["id"] = ego_vehicle_id
            ego_vehicle_dic["initial_position"] = initial_position
            ego_vehicle_dic["lanelet_id"] = ego_vehicle_lanelet_ids
            ego_vehicle_dic_list.append(ego_vehicle_dic)
            
        self.ego_vehicle_dic_list = ego_vehicle_dic_list
        return ego_vehicle_dic