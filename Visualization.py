##########################################################################################################################
##########################################################################################################################
##########################   VISUALIZATION   #############################################################################
##########################################################################################################################
##########################################################################################################################

class VisualizationFunctions:
    
    def __init__(self, scenario_graph):
        
        self.scenario_graph = scenario_graph
        self.first_group_id = dict()
        self.unique_group_ids = dict()
        
        self.group_arrays_len_dict = dict()
        self.vehicle_id_group_id = dict()
        self.group_id_vehicle_ids = dict()
        self.discovered_vehicles = dict()
        
        self.group_id_vehicle_ids_in_time_step = dict()
        self.all_groups = dict()
        self.__GetGroupsInTimeStep()
        
        #vehicle_id_group_id_in_time_step = dict() #we do not need it
        
    #######################################################################################################################
    #######################################################################################################################
    ###########################            Group Array for One Group           ############################################
    #######################################################################################################################
    ##############################################################################
    ########  __CollectGroupArrayConstructers():                        ##########
    ########      Collect the group arrays of vehicle                   ########## 
    ########      from __CollectGroupArrayConstructers in Vehicle class ##########
    ##############################################################################
    def __CalculateLengthOfGroupArrays(self,current_time):
        
        group_arrays_len_dict = dict()
        group_arrays_len_dict_current_time = dict()
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        
        for vehicle_id in vehicle_objects:
            if current_time in vehicle_objects[vehicle_id].group_array:
                group_array_len = len(vehicle_objects[vehicle_id].group_array[current_time])

                group_arrays_len_dict_current_time[vehicle_id] = group_array_len
                group_arrays_len_dict[current_time] = group_arrays_len_dict_current_time

        self.group_arrays_len_dict = group_arrays_len_dict
        
        return group_arrays_len_dict
    ##############################################################################
    def __IsTheExaminedVehicleFitWithAllOtherVehicles(self, examined_vehicle ,willing_ordered_group_array, current_time):
        
        isFit = True
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        fitting_rate = 0
        not_fit = 0
        fit = 0
        
        #check the vehicle in the all group arrays of vehicles in the group array of current_vehicle
        for vehicle_id in willing_ordered_group_array:
            if examined_vehicle not in vehicle_objects[vehicle_id].group_array[current_time] and vehicle_id != examined_vehicle:
                not_fit = not_fit + 1
            else:
                fit = fit + 1
                
        if not_fit != 0 :
            fit_ratio = fit / not_fit     
            if fit_ratio < 1:
                isFit = False
        
        return isFit
    ##############################################################################
    def __RemoveTheGroupedVehicles(self, ordered_group_aray,current_time):
        
        vehicles_willing_to_make_a_group = ordered_group_aray
        discovered_vehicles = self.discovered_vehicles
        
        #remove the vehicles has already has a group id
        for vehicle_id in ordered_group_aray:
            if current_time in discovered_vehicles and vehicle_id in discovered_vehicles[current_time]:
                vehicle_index = vehicles_willing_to_make_a_group.index(vehicle_id)
                vehicles_willing_to_make_a_group.pop(vehicle_index)
        
        return vehicles_willing_to_make_a_group
    ##############################################################################
    def __OrderVehicles(self, group_array, current_time):
        
        import operator
        
        #(ascending) order the vehicles according to size of vehicles in theier group_array
        ordered_group_array = []
        
        group_arrays_len_dict = self.group_arrays_len_dict
        temp_ordered_group_array = dict(sorted(group_arrays_len_dict[current_time].items(), key=operator.itemgetter(1))).keys()
        
        for vehicle_id in temp_ordered_group_array:
            if vehicle_id in group_array:
                ordered_group_array.append(vehicle_id)
        
        return ordered_group_array
    
    ##############################################################################
    def __GetFitVehicles(self, current_time_group_array, current_time):
        fit_vehicles = []
        discovered_vehicles = self.discovered_vehicles
        
        #order the vehicles according to size of vehicle in their goup array
        ordered_group_aray = self.__OrderVehicles(current_time_group_array, current_time)
        #remove the vehicles has already grouped
        willing_ordered_group_array = self.__RemoveTheGroupedVehicles(ordered_group_aray, current_time)
        
        #get the vehicles fit with each of the vehicles in the group_array of current_vehicle
        for examined_vehicle in willing_ordered_group_array:
            isFit = self.__IsTheExaminedVehicleFitWithAllOtherVehicles(examined_vehicle ,willing_ordered_group_array, current_time)
            if isFit:
                fit_vehicles.append(examined_vehicle)
                if current_time in discovered_vehicles:
                    discovered_vehicles[current_time].append(examined_vehicle)
                else:
                    discovered_vehicles[current_time] = [examined_vehicle]
                
        self.discovered_vehicles = discovered_vehicles
        return fit_vehicles
    ##############################################################################
    def __SetTheVehiclesGroupsDicts(self, current_vehicle_id, fit_vehicles_for_group, current_time):
        vehicle_id_group_id = self.vehicle_id_group_id
        group_id_vehicle_ids = self.group_id_vehicle_ids
        group_id = self.__GroupUniqueIDGenerator(current_time)
        fit_vehicles_for_group
        
        if current_time not in group_id_vehicle_ids:
            group_id_vehicle_ids[current_time] = {}
            group_id_vehicle_ids[current_time][group_id] = fit_vehicles_for_group
        else: 
            group_id_vehicle_ids[current_time][group_id] = fit_vehicles_for_group
            
        for vehicle_id in fit_vehicles_for_group:
            if current_time not in vehicle_id_group_id:
                vehicle_id_group_id[current_time] = {}
                vehicle_id_group_id[current_time][vehicle_id] = group_id
            else: 
                vehicle_id_group_id[current_time][vehicle_id] = group_id        
        
        self.vehicle_id_group_id = vehicle_id_group_id
        self.group_id_vehicle_ids = group_id_vehicle_ids
    ##############################################################################
    def __SetGroupIds(self, current_time):
        
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        discovered_vehicles = self.discovered_vehicles
        grouped_vehicles = []
        
        #TODO
        #vehicle_objects[current_vehicle_id].group_array --> am I need to order it
        for current_vehicle_id in vehicle_objects:
            if current_time not in discovered_vehicles or current_vehicle_id not in discovered_vehicles[current_time]:
                if current_time in vehicle_objects[current_vehicle_id].group_array:
                    current_time_group_array = vehicle_objects[current_vehicle_id].group_array[current_time]
                    #get the vehicles which fit with all vehicles in the group array
                    fit_vehicles_for_group = self.__GetFitVehicles(current_time_group_array, current_time)

                    if len(fit_vehicles_for_group) != 0:
                        grouped_vehicles.append(fit_vehicles_for_group)
                        self.__SetTheVehiclesGroupsDicts(current_vehicle_id, fit_vehicles_for_group, current_time)
                
                #put the current vehicle into discovered_vehicle if it has a group_id
                if current_time in self.vehicle_id_group_id and current_vehicle_id in self.vehicle_id_group_id[current_time]:
                    discovered_vehicles[current_time].append(current_vehicle_id)
        
        #put the each remaining vehicles into different groups. Each group is consist of 1 vehicle.
        # remaining vehicles mean is vehicles did not cooperate with any group
        for current_vehicle_id in vehicle_objects:
            if current_time not in discovered_vehicles or current_vehicle_id not in discovered_vehicles[current_time]:
                current_time_group_array = [current_vehicle_id]
                    #get the vehicles which fit with all vehicles in the group array
                fit_vehicles_for_group = self.__GetFitVehicles(current_time_group_array, current_time)

                if len(fit_vehicles_for_group) != 0:
                    grouped_vehicles.append(fit_vehicles_for_group)
                    self.__SetTheVehiclesGroupsDicts(current_vehicle_id, fit_vehicles_for_group, current_time)
                
                #put the current vehicle into discovered_vehicle if it has a group_id
                if current_time in self.vehicle_id_group_id and current_vehicle_id in self.vehicle_id_group_id[current_time]:
                    discovered_vehicles[current_time].append(current_vehicle_id)
                
            
        
        self.discovered_vehicles = discovered_vehicles
    
    ##############################################################################
    ###########  __GroupUniqueIDGenerator(): generate a new unique################
    ###########  id for vehicles' group                           ################
    ##############################################################################
    def __GroupUniqueIDGenerator(self, current_time):
        
        #take current ids
        first_group_id = self.first_group_id
        unique_group_ids = self.unique_group_ids

        if current_time not in first_group_id or  first_group_id[current_time] is None:
            #set first ego vehicle id if it is none and return the id
            first_group_id[current_time] = 1
            #add the new id to list of the ego vehicle ids
            if current_time in unique_group_ids:
                unique_group_ids[current_time].append(first_group_id[current_time])
            else:
                unique_group_ids[current_time] = [first_group_id[current_time]]
                
            #update constructor attributes
            self.first_group_id[current_time] = first_group_id[current_time]
            self.unique_group_ids = unique_group_ids
            
            return first_group_id[current_time]
        
        #find a new unique id
        new_id = first_group_id[current_time]
        while new_id in unique_group_ids[current_time]:
            new_id = new_id + 1
        
        #add the new id to list of the ego vehicle ids
        if current_time in unique_group_ids:
            unique_group_ids[current_time].append(new_id)
        else:
            unique_group_ids[current_time] = [new_id]
            
        #update constructor attributes
        self.first_group_id = first_group_id
        self.unique_group_ids = unique_group_ids
        
        return new_id
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    ##########################################################################################################################
    # shape of group_id_vehicle_ids_in_time_step
    #{time: {group_id: [group1], group_id: [group2]}}
    def __GetGroupsInTimeStep(self):
        
        all_groups = dict()
        group_id_vehicle_ids_in_time_step = self.group_id_vehicle_ids_in_time_step
        #TODO give scenario to __SetGroupIds in time steps
        
        for current_time in range (0,50): #TOFO define the dynamic currnet_time
            self.__CalculateLengthOfGroupArrays(current_time) # 1
            self.__SetGroupIds(current_time)
            group_id_vehicle_ids_in_time_step[current_time] = self.group_id_vehicle_ids[current_time]
            all_groups[current_time] = list(self.group_id_vehicle_ids[current_time].values())
        print(all_groups)
        self.all_groups = all_groups
        self.group_id_vehicle_ids_in_time_step = group_id_vehicle_ids_in_time_step
        