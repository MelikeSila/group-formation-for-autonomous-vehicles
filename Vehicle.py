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
    
    def __init__(self, vehicle_obstacle_info, vehicle_graph=1, w_vel=-1, w_dist=-1, w_size=-1, ideal_size=10, scorelimit=-20):
        
        from Sensor import DistanceSensor
        
        self.vehicle_info = vehicle_obstacle_info
        self.vehicle_initial_state = vehicle_obstacle_info["initial_state"]
        self.vehicle_graph =  vehicle_graph


        # distance_sensor is an Sensor object which include the id of the vehicles in range of the given vehicle sensor
        self.distance_sensor = DistanceSensor(self.vehicle_info, vehicle_graph,0)

        #weights and ideal groupsizes
        self.w_vel=w_vel
        self.w_dist=w_dist
        self.w_size=w_size
        self.ideal_size=ideal_size
        self.scorelimit=scorelimit
        
        #set arrays of vehicle
        self.score_dict = dict()
        self.group_array = dict()
        
        #knowledge base
        self.knowledge_base = None
        
    def _ScoreDictConstructor(self, vehicle_objects_dict, current_time):

        score_dict = {}
        scenario_graph = self.vehicle_graph

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
            self.distance_sensor.current_time = current_time
            if ID in self.distance_sensor.vehicles_in_range:
                add_dist=self.w_dist*scenario_graph.D(ID, self.vehicle_info["id"], current_time)
                add_vel=self.w_vel*rel_vel_vehicle.rel_vel_2_vehicles(state, self.vehicle_initial_state)
                add_vel=0
                score=add_vel+add_dist
                
                if current_time not in score_dict:
                    score_dict[current_time] = {ID: score}
                else:
                    score_dict[current_time].update({ID: score})

        #adds group size score
        
        if current_time in score_dict:
            score_dict[current_time] = add_group_size(score_dict[current_time], self.w_size, self.ideal_size)
        else:
            score_dict[current_time] = {}



        ########################################################
        return score_dict[current_time]

    def _GroupArrayConstructor(self, vehicle_objects_dict, current_time):

        for key, value in self.score_dict[current_time].items():
            if value>self.scorelimit:

                if (vehicle_objects_dict[key].handle_group_request(self.vehicle_info["id"], current_time)==1):
                    if current_time in self.group_array and key not in self.group_array[current_time]:
                        self.group_array[current_time].append(key)
                    else:
                        self.group_array[current_time] = [key]



        ########################################################




    def handle_group_request(self, ID, current_time):
        if current_time in self.score_dict:
            if self.score_dict[current_time][ID]>self.scorelimit:
                if current_time in self.group_array.keys() and ID not in self.group_array[current_time]:
                    self.group_array[current_time].append(ID)
                else:
                    self.group_array[current_time] = [ID]
                return 1
        else:
            return 0