import os
path_up = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
import sys
sys.path.insert(1, path_up)

from .possible_group_assignments import all_group_assignments
from rel_vel import rel_vel_measure
from group_size_measure import group_size_measure

#returns two lists: one with all the possible group assignments, the other with the scores of each assignment
def get_assignments_scores(planning_problem_set, id_list, ideal_group_size, w_size, w_vel):
    possible_assignments = all_group_assignments(id_list)
    assignment_scores =[]
    for assignments in possible_assignments:
        score=0
        for groups in assignments:
            #calculate scores for each group within this assignemt
            add_size=group_size_measure.group_size_measure(groups,ideal_group_size)
            add_vel=rel_vel_measure.rel_vel_measure(planning_problem_set, groups)
            #so far only group size
            score=score+(w_size*add_size)+(w_vel*add_vel)
            #adds up all the scores of the groups in one assignment
        assignment_scores.append(score)

    return possible_assignments, assignment_scores

def get_best_assignment(possible_assignments, assignment_scores):
    best=assignment_scores.index(max(assignment_scores))
    best_assignment=possible_assignments[best]

    return best_assignment
