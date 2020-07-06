##############################################################################
##########################    Vehicle Creating    ############################
##############################################################################
#### input:                                                                ###
####       vehicle_obstacle_dict: ScenarioGraph.ego_vehicles_dic ||        ###
####                              ScenarioGraph.obstacle_dic               ###
##############################################################################
class DistanceSensor:
    
    def __init__(self, vehicle_info, vehicle_graph, sensor_range):
        
        self.sensor_range = sensor_range
        self.vehicle_graph = vehicle_graph
        self.vehicle_info = vehicle_info
        
        self.vehicles_in_range = self.__FindVehiclesInRange()
    
    ##############################################################################
    #######  __FindVehiclesInRange: find the vehicles in the given range  ########
    ##############################################################################
    def __FindVehiclesInRange(self):
        
        sensor_range = self.sensor_range
        vehicles_in_range_array = []
        vehicle_graph = self.vehicle_graph
        vehicle_ids = vehicle_graph.ego_vehicle_ids + vehicle_graph.obstacle_ids
        vehicle_dict = {**vehicle_graph.ego_vehicles_dic, **vehicle_graph.obstacles_dic}
        vehicle = self.vehicle_info
        current_vehicle_id = vehicle["id"]
        
        for vehicle_id in vehicle_ids:
            
            distance = vehicle_graph.D(current_vehicle_id, vehicle_id)
            
            if distance < self.sensor_range:
                vehicles_in_range_array.append(vehicle_id)
        
        return vehicles_in_range_array
        