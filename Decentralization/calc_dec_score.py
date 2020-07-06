import os
path_up = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
import sys
sys.path.insert(1, path_up)

from rel_vel import rel_vel_measure
from group_size_measure import group_size_measure
import GroupDistance
import Convert_groups

def calc_array_for_each_vehicle(scenario, planning_problem_set, ideal_group_size, w_size, w_vel, w_dist):
    veh_list = list(planning_problem_set.planning_problem_dict.values()) + scenario.dynamic_obstacles

    array_list=[]

    for veh in veh_list:
        veh_array=[]
        for other_veh in veh_list:
            IDs=Convert_groups.conv_to_IDs([veh, other_veh])
            if other_veh!=veh:
                add_vel=rel_vel_measure.rel_vel_measure(planning_problem_set, scenario, [veh, other_veh])

                add_dist=GroupDistance.group_dist(scenario, IDs)
                score=w_vel*add_vel+w_dist*add_dist
            veh_array.append(other_veh: "score")
        #include group_size
        

        array_list.append(veh_array)





