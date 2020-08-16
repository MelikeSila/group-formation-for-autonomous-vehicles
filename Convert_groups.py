import commonroad.planning.planning_problem as planning_problem
import commonroad.planning as planning
def conv_to_IDs(scenario, planningProblemSet, veh_list):
    #reads in an object list and returns and ID_list
    ID_list=[]
    for veh in veh_list:
        if isinstance(veh, planning.planning_problem.PlanningProblem):
            ID_list.append(veh.planning_problem_id)
        else:
            ID_list.append(veh.obstacle_id)
    return ID_list


def conv_to_obj(scenario, planningProblemSet, ID_list):
    #reads in an ID_list and returns an objectlist
    veh_list=[]
    for ID in ID_list:
        if ID in planningProblemSet.planning_problem_dict:
            veh_list.append(planning_problem.PlanningProblemSet.find_planning_problem_by_id(planningProblemSet, ID))
        else:
            for obstacle in scenario.obstacles:
                if obstacle.obstacle_id==ID:
                    veh_list.append(obstacle)

    return veh_list