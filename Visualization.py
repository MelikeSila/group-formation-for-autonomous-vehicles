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
        
        self.vehicle_id_group_ids = dict()
        self.group_ids_vehicle_id = dict()
        
    #######################################################################################################################
    #######################################################################################################################
    ###########################            Group Array          ###########################################################
    #######################################################################################################################
    ##############################################################################
    ########  __CollectGroupArrayConstructers():                        ##########
    ########      Collect the group arrays of vehicle                   ########## 
    ########      from __CollectGroupArrayConstructers in Vehicle class ##########
    ##############################################################################
    def __IsTheCarWillingToCooperate(self, examined_vehicle_id, current_vehicle_id, discovered_vehicles):
        
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        
        examined_vehicle_group_array = vehicle_objects[examined_vehicle_id].group_array
        if examined_vehicle_id not in discovered_vehicles and current_vehicle_id in examined_vehicle_group_array:
            return True
        else:
            return False
    
    def __PutTheVehiclesInSameGroup(self, current_vehicle_id, examined_vehicle_id):
        #TODO
        vehicle_id_group_ids = self.vehicle_id_group_ids
        group_ids_vehicle_id = self.group_ids_vehicle_id
        
        if current_vehicle_id in vehicle_id_group_ids.keys() and examined_vehicle_id not in vehicle_id_group_ids.keys():
            #if current_vehicle_id exist and examined_vehicle_id not exist
            group_id = vehicle_id_group_ids[current_vehicle_id]
            group_ids_vehicle_id[group_id].append(examined_vehicle_id)
            vehicle_id_group_ids[ examined_vehicle_id ] = group_id
            
        elif examined_vehicle_id in vehicle_id_group_ids.keys() and current_vehicle_id not in vehicle_id_group_ids.keys():
            #if examined_vehicle_id exist and current_vehicle_id not exist
            group_id = vehicle_id_group_ids[examined_vehicle_id]
            group_ids_vehicle_id[group_id].append(current_vehicle_id)
            vehicle_id_group_ids[ current_vehicle_id ] = group_id
            
        else:
            #create a new id
            group_id = self.__GroupUniqueIDGenerator()
            group_ids_vehicle_id[group_id] = examined_vehicle_id
            group_ids_vehicle_id[group_id].append(current_vehicle_id)
            vehicle_id_group_ids[current_vehicle_id] = group_id
            vehicle_id_group_ids[examined_vehicle_id] = group_id
            
        self.vehicle_id_group_ids = vehicle_id_group_ids
        self.group_ids_vehicle_id = group_ids_vehicle_id
        
        
    def __SetGroupIds(self):
        
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        discovered_vehicles = []
        is_current_vehicle_find_group = 0
        
        vehicle_id_group_ids = self.vehicle_id_group_ids
        group_ids_vehicle_id = self.group_ids_vehicle_id
        
        for current_vehicle_id in vehicle_objects:
            
            discovered_vehicles.append(current_vehicle_id)
            group_array = vehicle_objects[current_vehicle_id].group_array
            
            #check the vehicles is want to make a gruop with current vehicle
            for examined_vehicle_id in group_array:
                
                isWilling = self.__IsTheCarWillingToCooperate(examined_vehicle_id, current_vehicle_id, discovered_vehicles)
                #check the examined_vehicle_id and current_vehicle_id in the same group
                if isWilling:
                    #they are willing to cooperate put them same group
                    self.__PutTheVehiclesInSameGroup(current_vehicle_id, examined_vehicle_id)
                    is_current_vehicle_find_group = 1
            
            #if the vehicle cannot cooperate any car put the vehicle into a new group
            if  not is_current_vehicle_find_group:
                #put the vehicle into new group
                group_id = self.__GroupUniqueIDGenerator()
                group_ids_vehicle_id[group_id].append(current_vehicle_id)
                vehicle_id_group_ids[current_vehicle_id] = group_id
        
        self.vehicle_id_group_ids = vehicle_id_group_ids
        self.group_ids_vehicle_id = group_ids_vehicle_id
    
    
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