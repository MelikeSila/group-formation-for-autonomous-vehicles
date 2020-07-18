##############################################################################
##########################    Vehicle Creating    ############################
##############################################################################
#### input:                                                                ###
####       vehicle_obstacle_dict: ScenarioGraph.ego_vehicles_dic ||        ###
####                              ScenarioGraph.obstacle_dic               ###
##############################################################################
class DistanceSensor:
    
    def __init__(self, vehicle_info, vehicle_graph):
        
        self.sensor_range = 50
        self.vehicle_graph = vehicle_graph
        self.vehicle_info = vehicle_info
        
        self.vehicles_in_range = self.__FindVehiclesInRange()
    
    ##############################################################################
    #######  __FindVehiclesInRange: find the vehicles in the given range  ########
    ##############################################################################
    def __FindVehiclesInRange(self):
        
        import math
        
        sensor_range = self.sensor_range
        vehicles_in_range_array = []
        vehicle_graph = self.vehicle_graph
        
        vehicle_ids = vehicle_graph.ego_vehicle_ids + vehicle_graph.obstacle_ids
        vehicle_dict = {**vehicle_graph.ego_vehicles_dic, **vehicle_graph.obstacles_dic}
        
        vehicle = self.vehicle_info
        current_vehicle_id = vehicle["id"]
        
        for vehicle_id in vehicle_dict:
            
            if vehicle_id != current_vehicle_id:
                
                #x0 = vehicle_dict[vehicle_id]["initial_position"][0]
                #y0 = vehicle_dict[vehicle_id]["initial_position"][1]
                #x1 = vehicle["initial_position"][0]
                #y1 = vehicle["initial_position"][1]
                #distance = math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
                distance = vehicle_graph.D(vehicle_id, current_vehicle_id )
                
                if distance < self.sensor_range:
                    vehicles_in_range_array.append(vehicle_id)
        
        return vehicles_in_range_array
        