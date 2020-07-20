##########################################################################################################################
##########################################################################################################################
##########################   VISUALIZATION   #############################################################################
##########################################################################################################################
##########################################################################################################################

class VisualizationFunctions:
    
    def __init__(self, scenario_graph):
        
        self.scenario_graph = scenario_graph
        self.first_group_id = None
        self.unique_group_ids = list()
        
        group_arrays_len_dict = self.__CalculateLengthOfGroupArrays()
        self.vehicle_id_group_id = dict()
        self.group_id_vehicle_ids = dict()
        self.discovered_vehicles = []
        self.__NewSetGroupIds()
        
    #######################################################################################################################
    #######################################################################################################################
    ###########################            Group Array          ###########################################################
    #######################################################################################################################
    ##############################################################################
    ########  __CollectGroupArrayConstructers():                        ##########
    ########      Collect the group arrays of vehicle                   ########## 
    ########      from __CollectGroupArrayConstructers in Vehicle class ##########
    ##############################################################################
    def __CalculateLengthOfGroupArrays(self):
        
        group_arrays_len_dict = dict()
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        
        for vehicle_id in vehicle_objects:
            group_array_len = len(vehicle_objects[vehicle_id].group_array)
            group_arrays_len_dict[vehicle_id] = group_array_len

        self.group_arrays_len_dict = group_arrays_len_dict
        
        return group_arrays_len_dict
    ##############################################################################
    def __IsTheExaminedVehicleFitWithAllOtherVehicles(self, examined_vehicle ,willing_ordered_group_array):
        
        isFit = True
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        
        #check the vehicle in the all group arrays of vehicles in the group array of current_vehicle
        for vehicle_id in willing_ordered_group_array:
            if examined_vehicle not in vehicle_objects[vehicle_id].group_array and vehicle_id != examined_vehicle:
                isFit = False
                return False
                
            
        return isFit
    ##############################################################################
    def __RemoveTheGroupedVehicles(self, ordered_group_aray):
        
        vehicles_willing_to_make_a_group = ordered_group_aray
        discovered_vehicles = self.discovered_vehicles
        
        #remove the vehicles has already has a group id
        for vehicle_id in ordered_group_aray:
            if vehicle_id in discovered_vehicles:
                vehicle_index = vehicles_willing_to_make_a_group.index(vehicle_id)
                vehicles_willing_to_make_a_group.pop(vehicle_index)
        
        return vehicles_willing_to_make_a_group
    ##############################################################################
    def __OrderVehicles(self, group_array):
        
        import operator
        
        #(ascending) order the vehicles according to size of vehicles in theier group_array
        ordered_group_array = []
        
        group_arrays_len_dict = self.group_arrays_len_dict
        temp_ordered_group_array = dict(sorted(group_arrays_len_dict.items(), key=operator.itemgetter(1))).keys()
        
        for vehicle_id in temp_ordered_group_array:
            if vehicle_id in group_array:
                ordered_group_array.append(vehicle_id)
        
        return ordered_group_array
    
    ##############################################################################
    def __GetFitVehicles(self, group_array):
        fit_vehicles = []
        discovered_vehicles = self.discovered_vehicles
        
        #order the vehicles according to size of vehicle in their goup array
        ordered_group_aray = self.__OrderVehicles(group_array)
        #remove the vehicles has already grouped
        willing_ordered_group_array = self.__RemoveTheGroupedVehicles(ordered_group_aray)
        
        #get the vehicles fit with each of the vehicles in the group_array of current_vehicle
        for examined_vehicle in willing_ordered_group_array:
            isFit = self.__IsTheExaminedVehicleFitWithAllOtherVehicles(examined_vehicle ,willing_ordered_group_array)
            if isFit:
                fit_vehicles.append(examined_vehicle)
                discovered_vehicles.append(examined_vehicle)
                
        self.discovered_vehicles = discovered_vehicles
        return fit_vehicles
    ##############################################################################
    def __SetTheVehiclesGroupsDicts(self, current_vehicle_id, fit_vehicles_for_group):
        vehicle_id_group_id = self.vehicle_id_group_id
        group_id_vehicle_ids = self.group_id_vehicle_ids
        group_id = self.__GroupUniqueIDGenerator()
        
        group_id_vehicle_ids[group_id] = fit_vehicles_for_group
        
        for vehicle_id in fit_vehicles_for_group:
            vehicle_id_group_id[vehicle_id] = group_id
        
        
        self.vehicle_id_group_id = vehicle_id_group_id
        self.group_id_vehicle_ids = group_id_vehicle_ids
    ##############################################################################
    def __NewSetGroupIds(self):
        
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        discovered_vehicles = self.discovered_vehicles
        grouped_vehicles = []
        
        #TODO
        #vehicle_objects[current_vehicle_id].group_array --> am I need to order it
        for current_vehicle_id in vehicle_objects:
            if current_vehicle_id not in discovered_vehicles:
                
                group_array = vehicle_objects[current_vehicle_id].group_array
                #get the vehicles which fit with all vehicles in the group array
                fit_vehicles_for_group = self.__GetFitVehicles(group_array)
                
                if len(fit_vehicles_for_group) != 0:
                    grouped_vehicles.append(fit_vehicles_for_group)
                    self.__SetTheVehiclesGroupsDicts(current_vehicle_id, fit_vehicles_for_group)
                #put the current vehicle into discovered_vehicle if it has a group_id
                if current_vehicle_id in self.vehicle_id_group_id.keys():
                    discovered_vehicles.append(current_vehicle_id)
            
        self.discovered_vehicles = discovered_vehicles
    
    ##############################################################################
    ###########  __GroupUniqueIDGenerator(): generate a new unique################
    ###########  id for vehicles' group                           ################
    ##############################################################################
    def __GroupUniqueIDGenerator(self):
        
        #take current ids
        first_group_id = self.first_group_id
        unique_group_ids = self.unique_group_ids

        if first_group_id is None:
            #set first ego vehicle id if it is none and return the id
            first_group_id = 1
            #add the new id to list of the ego vehicle ids
            unique_group_ids.append(first_group_id)
            #update constructor attributes
            self.first_group_id = first_group_id
            self.unique_group_ids = unique_group_ids
            
            return first_group_id
        
        #find a new unique id
        new_id = first_group_id
        while new_id in unique_group_ids:
            new_id = new_id + 1
        
        #add the new id to list of the ego vehicle ids
        unique_group_ids.append(new_id)
        #update constructor attributes
        self.first_group_id = first_group_id
        self.unique_group_ids = unique_group_ids
        
        return new_id
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################