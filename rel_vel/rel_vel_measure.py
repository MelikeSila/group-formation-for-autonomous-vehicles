from .rel_vel_group import calc_rel_vel_group
import commonroad.planning.planning_problem as planning_problem


def rel_vel_measure(id_set):
    # uses the IDs of the vehicles to get the states of the vehicles and than
    # uses calc_rel_vel_group to get rel_vel
    state_list = []
    print(id_set)
    # transform ID_list to state_list
    for x in id_set:
        # print(x)
        prob = planning_problem.PlanningProblemSet.find_planning_problem_by_id(x)
        state_list.append(prob.initial_state)
        print(state_list)

    # calculate velocity measure
    vel_measure = calc_rel_vel_group(state_list)

    return vel_measure
