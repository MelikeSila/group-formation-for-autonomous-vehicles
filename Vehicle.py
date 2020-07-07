##############################################################################
##########################    Vehicle Creating    ############################
##############################################################################
#### input:                                                                ###
####       vehicle_obstacle_info: ScenarioGraph.ego_vehicles_dic ||        ###
####                              ScenarioGraph.obstacle_dic               ###
##############################################################################
import numpy as np

class Vehicle:
    
    def __init__(self, vehicle_obstacle_info, vehicle_graph):
        
        from Sensor import DistanceSensor
        
        self.vehicle_info = vehicle_obstacle_info
        self.vehicle_graph =  vehicle_graph
        
        # distance_sensor is an Sensor object which include the id of the vehicles in range of the given vehicle sensor
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

        add_group_size(score_array, w_group, ideal_size):
            sorted_score_array{k: v for k, v in sorted(score_array.items(), key=lambda item: item[1])}
            for i in range(0,len(score_array)):
                sorted_score_array.values()[i]=sorted_score_array[i]+((i+1-ideal_size)++2)*np.sign(i+1-ideal_size)


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