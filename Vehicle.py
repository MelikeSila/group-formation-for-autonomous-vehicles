##############################################################################
##########################    Vehicle Creating    ############################
##############################################################################
#### input:                                                                ###
####       vehicle_obstacle_info: ScenarioGraph.ego_vehicles_dic ||        ###
####                              ScenarioGraph.obstacle_dic               ###
##############################################################################
class Vehicle:
    
    def __init__(self, vehicle_obstacle_info, vehicle_graph):
        
        from Sensor import DistanceSensor
        
        self.vehicle_info = vehicle_obstacle_info
        self.vehicle_graph =  vehicle_graph
        
        # set sensors of vehicle
        self.distance_sensor = DistanceSensor(self.vehicle_info, vehicle_graph)
        
        #set arrays of vehicle
        self.score_array = self.__ScoreArrayConstructer()
        self.group_array = self.__GroupArrayConstructer()
        
        #knowledge base
        self.knowledge_base = None
        
    def __ScoreArrayConstructer(self):

        score_array = []
        distance_sensor = self.distance_sensor

        ########################################################
        ## TODO: calculate the score array of the given vehiclee
        ########################################################

        score_array = None

        ########################################################
        return score_array

    def __GroupArrayConstructer(self):

        group_array = []
        distance_sensor = self.distance_sensor

        ########################################################
        ## TODO: calcuşate the group array of the vehicle
        ########################################################

        group_array = None

        ########################################################


        return group_array            