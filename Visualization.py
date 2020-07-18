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
        
        self.vehicle_id_group_id = dict()
        self.group_id_vehicle_ids = dict()
        self.__SetGroupIds()
        
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
    ##############################################################################
    ##############################################################################
    ##############################################################################
    def __PutTheVehiclesInSameGroup(self, current_vehicle_id, examined_vehicle_id):
        #TODO
        vehicle_id_group_id = self.vehicle_id_group_id
        group_id_vehicle_ids = self.group_id_vehicle_ids
        
        #if current_vehicle_id has a group id
        if current_vehicle_id in vehicle_id_group_id.keys() and examined_vehicle_id not in vehicle_id_group_id.keys():
            #if current_vehicle_id exist and examined_vehicle_id not exist
            group_id = vehicle_id_group_id[current_vehicle_id]
            group_id_vehicle_ids[group_id].append(examined_vehicle_id)
            vehicle_id_group_id[ examined_vehicle_id ] = group_id
        
        #if examined_vehicle_id has a group id
        elif examined_vehicle_id in vehicle_id_group_id.keys() and current_vehicle_id not in vehicle_id_group_id.keys():
            #if examined_vehicle_id exist and current_vehicle_id not exist
            group_id = vehicle_id_group_id[examined_vehicle_id]
            group_id_vehicle_ids[group_id].append(current_vehicle_id)
            vehicle_id_group_id[ current_vehicle_id ] = group_id
            
        #if both of them don't have a group id
        elif examined_vehicle_id not in vehicle_id_group_id.keys() and current_vehicle_id not in vehicle_id_group_id.keys():
            #create a new id
            group_id = self.__GroupUniqueIDGenerator()
            group_id_vehicle_ids[group_id] = [examined_vehicle_id]
            group_id_vehicle_ids[group_id].append(current_vehicle_id)
            vehicle_id_group_id[current_vehicle_id] = group_id
            vehicle_id_group_id[examined_vehicle_id] = group_id
        #if they are not agree on the group id put the current_vehicle into a group if it doesn't have a group
        elif current_vehicle_id not in vehicle_id_group_id.keys():
            #if the vehicle cannot cooperate any car put the vehicle into a new group
            #put the vehicle into new group
            group_id = self.__GroupUniqueIDGenerator()
            group_id_vehicle_ids[group_id] = [ current_vehicle_id ]
            vehicle_id_group_id[current_vehicle_id] = group_id
            
        self.vehicle_id_group_id = vehicle_id_group_id
        self.group_id_vehicle_ids = group_id_vehicle_ids
    
    ##############################################################################
    ##############################################################################
    ##############################################################################   
    #def __CheckTheWillingVehiclesInGroupArrayHasGroup(self, current_vehicle_id, group_array, discovered_vehicles ):
        
     #   willing_vehicles_group_array = []
        
      #  for veh in group_array:
       #     if self.__IsTheCarWillingToCooperate(veh, current_vehicle_id, discovered_vehicles) :
        #        willing_vehicles_group_array.append(veh)
        
       # possible_groups = set(willing_vehicles_group_array).intersection(discovered_vehicles)
        
        #return possible_groups
        
    ##############################################################################
    ##############################################################################
    ##############################################################################    
    def __SetGroupIds(self):
        
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        discovered_vehicles = []
        
        for current_vehicle_id in vehicle_objects:
            
            discovered_vehicles.append(current_vehicle_id)
            group_array = vehicle_objects[current_vehicle_id].group_array
            
            #get the group ids of vehicle if the any vehicle in the group_array is assigned to a group
            #possible_groups = self.__CheckTheWillingVehiclesInGroupArrayHasGroup(current_vehicle_id, group_array, discovered_vehicles)
            
            #check the vehicles is want to make a gruop with current vehicle
            for examined_vehicle_id in group_array:
                
                isWilling = self.__IsTheCarWillingToCooperate(examined_vehicle_id, current_vehicle_id, discovered_vehicles)
                #check the examined_vehicle_id and current_vehicle_id in the same group
                if isWilling:
                    #they are willing to cooperate put them same group if they aggreed on group id
                    #otherwise put the current vehicle into a new group if it doesn't have a group
                    self.__PutTheVehiclesInSameGroup(current_vehicle_id, examined_vehicle_id)
            
    
    
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