import os
path_up = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
import sys
sys.path.insert(1, path_up)

from .possible_group_assignments import all_group_assignments
from rel_vel import rel_vel_measure
from group_size_measure import group_size_measure
import GroupDistance
import GraphBasedDistanceMeasure

#returns two lists: one with all the possible group assignments, the other with the scores of each assignment
def get_assignments_scores(scenario, planning_problem_set, ideal_group_size, w_size, w_vel, w_dist):

    veh_list=list(planning_problem_set.planning_problem_dict.values()) + scenario.dynamic_obstacles
    possible_assignments = all_group_assignments(veh_list)
    assignment_scores =[]
    ScenarioGraph = ScenarioGraph(scenario, planning_problem_set)
    G = ScenarioGraph.scenario_graph
    lanelets = ScenarioGraph.lanelets

    for assignments in possible_assignments:
        score=0
        for groups in assignments:
            #calculate scores for each group within this assignemt
            add_size=group_size_measure.group_size_measure(groups,ideal_group_size)
            add_vel=rel_vel_measure.rel_vel_measure(planning_problem_set, scenario, veh_list)
            add_dist=GroupDistance.group_dist(scenario, groups, ScenarioGraph)
            # adds up all the scores of the groups in one assignment and weighing them
            score=score+(w_size*add_size)+(w_vel*add_vel)+(w_dist*add_dist)


        assignment_scores.append(score)

    return possible_assignments, assignment_scores

#returns the groups assignment with the highest score (and returns the IDs of the objects)
def get_best_assignment(possible_assignments, assignment_scores):
    best=assignment_scores.index(min(assignment_scores))
    best_assignment=possible_assignments[best]
    best_assignment_IDs=[]
    for group in best_assignment:
        grouplist=[]
        for veh in group:
            try:
                x=veh.obstacle_id
            except:
                x=veh.planning_problem_id
            grouplist.append(x)
        best_assignment_IDs.append(grouplist)

    return best_assignment_IDs, best_assignment
