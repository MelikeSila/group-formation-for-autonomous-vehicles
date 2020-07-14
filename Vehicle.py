##############################################################################
##########################    Vehicle Creating    ############################
##############################################################################
#### input:                                                                ###
####       vehicle_obstacle_info: ScenarioGraph.ego_vehicles_dic ||        ###
####                              ScenarioGraph.obstacle_dic               ###
##############################################################################
import numpy as np
import commonroad.planning.planning_problem as planning_problem
import GraphBasedDistanceMeasure
import rel_vel
import numpy as np
from rel_vel import rel_vel_vehicle

class Vehicle:
    
    def __init__(self, vehicle_obstacle_info, vehicle_graph=1, w_vel=1, w_dist=1, w_size=1, ideal_size=1, scorelimit=1):
        
        from Sensor import DistanceSensor
        
        self.vehicle_info = vehicle_obstacle_info
        self.vehicle_initial_state = vehicle_obstacle_info["initial_state"]
        self.vehicle_graph =  vehicle_graph


        # distance_sensor is an Sensor object which include the id of the vehicles in range of the given vehicle sensor
        self.distance_sensor = DistanceSensor(self.vehicle_info, vehicle_graph)

        #weights and ideal groupsizes
        self.w_vel=w_vel
        self.w_dist=w_dist
        self.w_size=w_size
        self.ideal_size=ideal_size
        self.scorelimit=scorelimit
        
        #set arrays of vehicle
        self.score_dict = {}
        self.group_array = None
        
        #knowledge base
        self.knowledge_base = None
        
    def ScoreDictConstructor(self, vehicle_objects_dict, scenario_graph):

        score_dict = {}

        vehicle_objects=list(vehicle_objects_dict.values())
        #reads in score_dict (with missing group size features) and adds group size features
        def add_group_size(score_dict, w_size, ideal_size):
            sorted_score_dict = {k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1])}
            i=0
            for k, v in sorted_score_dict.items():
                v=sorted_score_dict[k]
                sorted_score_dict[k]=v+w_size*(((i+1-ideal_size)++2)*np.sign(i+1-ideal_size))

            return sorted_score_dict

        #iterates through vehicle list and calculates scores for the vehicles in range
        for vehicle in vehicle_objects:

            #gets state and ID of the vehicle for the distance and velocity functions

            ID=vehicle.vehicle_info["id"]
            state=vehicle.vehicle_initial_state

            #uses state and ID to calculate score
            if ID in self.distance_sensor.vehicles_in_range:
                add_dist=self.w_dist*scenario_graph.D(ID, self.vehicle_info["id"])
                add_vel=self.w_vel*rel_vel_vehicle.rel_vel_2_vehicles(state, self.vehicle_initial_state)
                add_vel=0
                score=add_vel+add_dist
                score_dict.update({ID: score})

        #adds group size score
        score_dict=add_group_size(score_dict, self.w_size, self.ideal_size)



        ########################################################
        return score_dict

    def GroupArrayConstructer(self):

        group_array = []
        distance_sensor = self.distance_sensor

        ########################################################
        ## TODO: calcuşate the group array of the vehicle
        ########################################################

        for veh in score_dict:
            if veh.value>self.scorelimit:
                if (veh.handle_group_request==1):
                    group_array.append(veh.key)




        ########################################################


        return group_array

    def handle_group_request(self, ID):
        pass
