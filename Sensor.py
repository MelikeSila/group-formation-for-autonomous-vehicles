##############################################################################
##########################    Vehicle Creating    ############################
##############################################################################
#### input:                                                                ###
####       vehicle_obstacle_dict: ScenarioGraph.ego_vehicles_dic ||        ###
####                              ScenarioGraph.obstacle_dic               ###
##############################################################################
class Sensor:
    
    def __init__(self, vehicle, vehicle_graph, sensor_range):
        
        self.sensor_range = sensor_range
        self.vehicles_in_range = self.__FindVehiclesInRange()
        self.vehicle = vehicle
    
    ##############################################################################
    ########    ##########
    ##############################################################################
    def __FindVehiclesInRange(self):
        
        sensor_range = self.sensor_range
        vehicles_in_range_array = []
        vehicle_graph = self.vehicle_graph
        vehicle_ids = vehicle_graph.ego_vehicle_ids + vehicle.obstacle_ids
        vehicle_dict = {**vehicle_graph.ego_vehicles_dic, **vehicle_graph.obstacles_dic}
        current_vehicle_id = self.vehicle["id"]
        
        for vehicle_id in vehicle_ids:
            distance = vehicle_graph.D(current_vehicle_id, vehicle_id)
            print(distance)
            if distance < 1000:
                vehicles_in_range_array.append(vehicle_id)
        print(vehicles_in_range_array)
        
        return vehicles_in_range_array
        