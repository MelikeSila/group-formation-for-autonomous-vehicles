from .possible_group_assignments import all_group_assignments
from .group_size_measure import group_size_measure
#returns two lists: one with all the possible group assignments, the other with the scores of each assignment
def get_assignments_scores(id_list):
    possible_assignments = all_group_assignments(id_list)
    assignment_scores =[]
    for assignments in possible_assignments:
        score=0
        for groups in assignments:
            #calculate scores for each group within this assignemt
            add=group_size_measure(groups,2)
            #so far only group size
            score=score+add
            #adds up all the scores of the groups in one assignment
        assignment_scores.append(score)

    return possible_assignments, assignment_scores

