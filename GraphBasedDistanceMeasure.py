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
        
        self.scenario_graph = self._CreateLaneletGraph()
        
        self.first_ego_vehicle_id = None
        
        self.ego_vehicle_ids = list()
        self.ego_vehicles_current_state_dic = dict()
        self.ego_vehicles_dic = self.__InitializeEgoVehicleAttributes()
        
        self.obstacle_ids = list()
        self.obstacles_current_state_dic = dict() #TODO
        self.obstacles_dic = self.__InitializeObstacleAttributes()
        
        #TODO open the comments after fic the ego_vehicle
        self.all_cars_dict = self.obstacles_dic #{ **self.ego_vehicles_dic, **self.obstacles_dic}
        self.all_cars_current_state_dict = self.obstacles_current_state_dic #{ **self.ego_vehicles_current_state_dic, **self.obstacles_current_state_dic}
        
        self.vehicle_objects_dict = self.__CreateVehcileObjects()
        
        self.current_time = 0
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
    #############  __InitializeObstacleLaneletNode(obstacle):        #############
    #############  return initial_lanelet, initial_node of obstacle  #############
    ##############################################################################
    def __InitializeObstacleLaneletNode(self, obstacle):
        
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
    #####  __InitializeEgoVehicleAttributes(self):                           #####
    #####  Initialize ego vehicles attributes;                               #####
    #####  (id, initial_position, initial_lanelet_id, initial_lanelet_node)  #####
    ##############################################################################
    def __InitializeEgoVehicleAttributes(self):
        
        from commonroad.scenario.lanelet import LaneletNetwork
        import numpy as numpy

        planning_problem_set = self.planning_problem_set
        ego_vehicles_dic = dict()

        for pp_key in planning_problem_set.planning_problem_dict:
            
            ego_vehicle_dic = dict()
            initial_position = list()
            #get initial_positions of the ego vehicle
            pp = planning_problem_set.planning_problem_dict[pp_key]
            initial_position.append(pp.initial_state.position)
            ego_vehicle_id = self.__GenerateNewEgoVehicleID()
            ego_vehicle_lanelet_ids = LaneletNetwork.find_lanelet_by_position( self.scenario.lanelet_network, 
                                                                              point_list = (initial_position ))[0][0]

            #set the ego vehicle initial state to ego_vehicle_dic
            ego_vehicle_dic["id"] = ego_vehicle_id
            ego_vehicle_dic["initial_position"] = numpy.array(initial_position)[0]
            ego_vehicle_dic["initial_state"] = pp.initial_state
            ego_vehicle_dic["initial_lanelet_id"] = ego_vehicle_lanelet_ids
            ego_vehicle_dic["initial_lanelet_node"] = 0
            ego_vehicle_dic["planning_problem_id"] = pp.planning_problem_id
            #TODO ego_vehicle_dic["current_state_dic"]
            #ego_vehicle_dic["current_state_dic"] = {0: 67, 1: 67, 2: 67, 3: 67, 4: 67, 5: 67, 6: 67, 7: 67, 8: 67, 9: 60, 10: 60, 11: 60, 12: 60, 13: 60, 14: 60, 15: 60, 16: 60, 17: 60, 18: 60, 19: 60, 20: 60, 21: 60, 22: 60, 23: 60, 24: 60, 25: 60, 26: 60, 27: 60, 28: 60, 29: 60, 30: 60, 31: 60, 32: 60, 33: 60, 34: 60, 35: 60, 36: 60, 37: 60, 38: 60, 39: 60, 40: 60, 41: 60, 42: 60, 43: 60, 44: 60, 45: 60, 46: 60, 47: 60}
            
            ego_vehicles_dic[ego_vehicle_id] = ego_vehicle_dic
            
        self.ego_vehicles_dic = ego_vehicles_dic
        
        return ego_vehicles_dic
    
    ##############################################################################
    #####  __InitializeObstacleAttributes(self):                             #####
    #####  Initialize obstacles  attributes;                                 #####
    #####  (id, initial_position, initial_lanelet_id, initial_lanelet_node)  #####
    ##############################################################################
    def __InitializeObstacleAttributes(self):
        
        obstacles = self.obstacles
        obstacles_dic = dict()
        obstacle_ids = list()
        obstacles_current_state_dic = self.obstacles_current_state_dic
        
        for obstacle in obstacles:
            
            obstacle_dic = dict()
            vertex, node = self.__InitializeObstacleLaneletNode(obstacle)
            o_id = obstacle.obstacle_id            
            
            #####################################################################
            #####################################################################
            #set the obstacles_current_state_dic
            from commonroad.scenario.lanelet import LaneletNetwork
            
            time = 0
            prev_lanelet = -1
            scenario = self.scenario
            current_state_dic = dict()
            while obstacle.occupancy_at_time(time):
                current_position = obstacle.occupancy_at_time(time).shape.center
                current_lanelet = LaneletNetwork.find_lanelet_by_position( scenario.lanelet_network,
                                                                           point_list = [current_position])[0][0]
                ####if prev_lanelet != current_lanelet:
                    #setting the current state dict with key lanelet
                current_state_dic[time] = self.__FindKeyGraphId(current_lanelet)
                #prev_lanelet = current_lanelet
               ####
                time = time + 1
            obstacles_current_state_dic[o_id] = current_state_dic
            #####################################################################
            #####################################################################
            
            obstacle_dic["id"] = obstacle.obstacle_id
            obstacle_dic["initial_position"] = obstacle.initial_state.position
            obstacle_dic["initial_state"] = obstacle.initial_state
            obstacle_dic["initial_lanelet_id"] = vertex
            obstacle_dic["initial_lanelet_node"] = node
            obstacle_dic["planning_problem_id"] = -1
            obstacle_dic["current_state_dic"] = current_state_dic
            obstacles_dic[o_id] = obstacle_dic
            obstacle_ids.append(o_id)
            
        self.obstacles_dic = obstacles_dic
        self.obstacle_ids = obstacle_ids
        
        self.obstacles_current_state_dic = obstacles_current_state_dic
        
        return obstacles_dic

    ##############################################################################
    #####  __CreateVehcileObjects(self):                                     #####
    #####  Initialize Vehicle objects from Vehicle class                     #####
    ##############################################################################
    def __CreateVehcileObjects(self):
        
        from Vehicle import Vehicle
        vehicle_objects_dict = dict()
        cars = self.all_cars_dict
        
        for car_id in cars:
            if car_id > 1: #I removed the ego vehicle for last demo
                vehicle_objects_dict[car_id] = Vehicle(cars[car_id], self)
        
        #calculate scoredict and grouparray for each time step
        #TODO
        for vehicle in vehicle_objects_dict.values():
            for current_time in vehicle.vehicle_info["current_state_dic"].keys():
                vehicle.score_dict[current_time]=vehicle._ScoreDictConstructor(vehicle_objects_dict, current_time)

        for vehicle in vehicle_objects_dict.values():
            for current_time in vehicle.vehicle_info["current_state_dic"].keys():
                vehicle._GroupArrayConstructor(vehicle_objects_dict, current_time)
            
        return vehicle_objects_dict
    
    ##########################################################################################################################
    #############################################  FUNCTIONS IN THE PAPER  ###################################################
    ##########################################################################################################################
    
    ##############################################################################
    ##############  V(id): return initial lanelet and node########################
    ##############################################################################
    def V(self,vehicle_obstacle_id):
        
        current_time = self.current_time
        
        vehicle_obstacle = self.all_cars_dict
        
        current_lanelet = vehicle_obstacle[vehicle_obstacle_id]["current_state_dic"][current_time]
        
        #current node
        if current_time == 0:
            current_node = vehicle_obstacle[vehicle_obstacle_id]["initial_lanelet_node"]
        else:
            current_node = 0
            
        return  current_lanelet ,current_node
    
    
    
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
    def D(self, c1, c2, current_time):
        assert c1 is not None and c2 is not None, "Id cannot be Null!"
        assert c1 in self.all_cars_dict and c2 in self.all_cars_dict, "One of the given ids is not defined in the Graph!"
        
        import math
        
        self.current_time = current_time
        
        #if one of the vehicle is not available anymore in the lanelet don't calculate the distance
        #e.g when cars go out the last lanelet of the graph
        vehicle_obstacle = self.all_cars_dict
        if current_time not in vehicle_obstacle[c1]["current_state_dic"] or current_time not in vehicle_obstacle[c2]["current_state_dic"]:
            return math.inf
        
        G = self.scenario_graph
        v1, n1 = self.V(c1)
        v2, n2 = self.V(c2)
        vm = self.M(v1, v2)  #TODO calculation of M may be easier

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