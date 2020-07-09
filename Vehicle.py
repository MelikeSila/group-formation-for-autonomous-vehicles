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

class Vehicle:
    
    def __init__(self, vehicle_obstacle_info, vehicle_graph):
        
        from Sensor import DistanceSensor
        
        self.vehicle_info = vehicle_obstacle_info
        self.vehicle_graph =  vehicle_graph

        #own ID regardless whether its planningProblem or obstacle
        if self.vehicle_info.id>0:
            self.ownID=self.vehicle_info.id
        else:
            self.ownID=self.vehicle_info.planning_problem_id
        
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
        vehicle_objects = SG.vehicle_objects_dict


        for vehicle in vehicle_objects:
            if vehicle_objects[vehicle].vehicle_info.id>o:
                ID=vehicle_objects[vehicle].vehicle_info.id
                state=
            else if vehicle_objects[vehicle].vehicle_info.planning_problem_id>0
                ID=vehicle_objects[vehicle].vehicle_info.planning_problem_id
                state=planning_problem.PlanningProblemSet.find_planning_problem_by_id(PlanningProblemSet, ID)
            if ID in self.distance_sensor.vehicles_in_range:
                add_dist=w_dist*GraphBasedDistanceMeasure.D(ID, self.ownID)
                add_vel=w_vel*rel_vel.rel_vel_vehicle(state, self.vehicle_info.state)




        def add_group_size(score_array, w_size, ideal_size):
            sorted_score_array{k: v for k, v in sorted(score_array.items(), key=lambda item: item[1])}
            for i in range(0,len(score_array)):
                sorted_score_array.values()[i]=sorted_score_array[i]+w_size(((i+1-ideal_size)++2)*np.sign(i+1-ideal_size))
            return sorted_score_array

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