##############################################################################
##########################    Vehicle Creating    ############################
##############################################################################
#### input:                                                                ###
####       vehicle_obstacle_dict: ScenarioGraph.ego_vehicles_dic ||        ###
####                              ScenarioGraph.obstacle_dic               ###
##############################################################################
class Vehicle:
    
    def __init__(self, vehicle_obstacle_dict, vehicle_graph = None):
        
        self.vehicle_info = vehicle_obstacle_dict
        self.vehicle_graph =  vehicle_graph
        self.sensor = Sensor(vehicle, vehicle_graph, sensor_range)
        self.score_array = None
        self.group_array = None
        self.knowledge_base = None
    
    ##############################################################################
    ########    ##########
    ##############################################################################