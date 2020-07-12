from commonroad.visualization.draw_dispatch_cr import draw_object
import commonroad.planning as planning
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection


def colorize_groups(group_assignment, axes):
    colors = ['#123456', '#000000', '#880000', '#008800', '#000088', '#994499', '#990022', '#998822']
    i = 0
    patch = []
    for group in group_assignment:
        color = colors[i % 8]
        draw_params = {'shape': {'facecolor': color}}
        for veh in group:
            if isinstance(veh, planning.planning_problem.PlanningProblem):
                patch.append(patches.Rectangle(veh.initial_state.position[0]-3.5, veh.initial_state.position[1]-1.5, 7, 3, veh.initial_state.orientation ))


            else:
                draw_object(veh, draw_params=draw_params)

        i = i + 1
    p = PatchCollection(patch)
    axes.add_collection(p)
    return None
