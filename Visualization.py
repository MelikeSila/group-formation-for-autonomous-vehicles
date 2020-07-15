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
        self.group_ids = self.__SetGroupIds()
        
        
    #######################################################################################################################
    #######################################################################################################################
    ###########################            Group Array          ###########################################################
    #######################################################################################################################
    ##############################################################################
    ########  __CollectGroupArrayConstructers():                        ##########
    ########      Collect the group arrays of vehicle                   ########## 
    ########      from __CollectGroupArrayConstructers in Vehicle class ##########
    ##############################################################################
    def __SetGroupIds(self):
        
        import numpy as np
        
        group_ids = dict()
        vehicle_objects = self.scenario_graph.vehicle_objects_dict
        
        for vehicle_dict_id in vehicle_objects:
            
            group_array = vehicle_objects[vehicle_dict_id].group_array

            if vehicle_dict_id not in group_array: group_array.append(vehicle_dict_id)
            group_array = np.sort(group_array)
            if vehicle_dict_id not in group_ids:
                for vc_id in vehicle_objects:

                    group_array2 = vehicle_objects[vc_id].group_array

                    if vc_id not in group_array2: group_array2.append(vc_id)
                    group_array2 = np.sort(group_array2)

                    if np.array_equal(np.array(group_array), np.array(group_array2)) and vehicle_dict_id != vc_id:
                        if vc_id in group_ids: #isGroupHasId(vc_id):
                            group_ids[vehicle_dict_id] = group_ids[vc_id]
                        else:
                            group_ids[vehicle_dict_id] = self.__GroupUniqueIDGenerator()
                            group_ids[vc_id] = group_ids[vehicle_dict_id]
            if vehicle_dict_id not in group_ids:
                group_ids[vehicle_dict_id] = self.__GroupUniqueIDGenerator()
        
        return group_ids
        
    
    
    
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