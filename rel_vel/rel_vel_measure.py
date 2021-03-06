from .rel_vel_group import calc_rel_vel_group
import commonroad.planning.planning_problem as planning_problem


def rel_vel_measure(planning_problem_set, scenario, group):
    # uses the IDs of the vehicles to get the states of the vehicles and then
    # uses calc_rel_vel_group to get rel_vel
    state_list = []
    
    # get a list of states of the group
    for x in group:
        
        #prob = planning_problem_set.find_planning_problem_by_id(x)
        state_list.append(x.initial_state)
       

    # calculate velocity measure
    vel_measure = calc_rel_vel_group(state_list)

    return vel_measure
