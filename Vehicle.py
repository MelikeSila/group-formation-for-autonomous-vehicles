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
    
    def __init__(self, vehicle_obstacle_info, vehicle_graph, w_vel, w_dist, w_size, ideal_size):
        
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

        #weights and ideal groupsizes
        self.w_vel=w_vel
        self.w_dist=w_dist
        self.w_size=w_size
        self.ideal_size=ideal_size
        
        #set arrays of vehicle
        self.score_dict = self.__ScoreDictConstructer()
        self.group_array = self.__GroupArrayConstructer()
        
        #knowledge base
        self.knowledge_base = None
        
    def __ScoreDictConstructer(self):

        score_dict = {}
        distance_sensor = self.distance_sensor

        ########################################################
        ## TODO: calculate the score array of the given vehiclee
        ########################################################
        vehicle_objects = SG.vehicle_objects_dict

        #reads in score_dict (with missing group size features) and adds group size features
        def add_group_size(score_dict, w_size, ideal_size):
            sorted_score_dict{k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1])}
            for i in range(0,len(score_array)):
                sorted_score_dict.values()[i]=sorted_score_dict[i]+w_size(((i+1-ideal_size)++2)*np.sign(i+1-ideal_size))
            return sorted_score_dict

        #
        for vehicle in vehicle_objects:
            if vehicle_objects[vehicle].vehicle_info.id>o:
                ID=vehicle_objects[vehicle].vehicle_info.id
                state=
            else if vehicle_objects[vehicle].vehicle_info.planning_problem_id>0
                ID=vehicle_objects[vehicle].vehicle_info.planning_problem_id
                state=planning_problem.PlanningProblemSet.find_planning_problem_by_id(PlanningProblemSet, ID)
            if ID in self.distance_sensor.vehicles_in_range:
                add_dist=self.w_dist*GraphBasedDistanceMeasure.D(ID, self.ownID)
                add_vel=self.w_vel*rel_vel.rel_vel_vehicle(state, self.vehicle_info.state)
                score=add_vel+add_dist
                score_dict.update(ID:'score')

        score_dict=add_group_size(score_dict, self.w_size, self.ideal_size)






        ########################################################
        return score_dict

    def __GroupArrayConstructer(self):

        group_array = []
        distance_sensor = self.distance_sensor

        ########################################################
        ## TODO: calcuşate the group array of the vehicle
        ########################################################


        group_array = None

        ########################################################


        return group_array            