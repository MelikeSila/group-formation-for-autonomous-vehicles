from commonroad.visualization.draw_dispatch_cr import draw_object
import commonroad.planning as planning
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection


def colorize_groups(group_assignment, axes, time, group_ids):
    colors = ['#f5fc00', '#00fcfb', '#56c933', '#035aff', '#fc4a00','#123456', '#c400fc', '#fca500', '#00fca3', '#71fff1', '#aebbff', '#C2185B', '#00796B', '#998822', '#880000', '#008800', '#000088', '#994499', '#990022', '#000000']
    i = 0
    patch = []
    for group in group_assignment:
        color = colors[i % 20]
        
        #{'shape': {'facecolor': color}}
        for veh in group:
            if isinstance(veh, planning.planning_problem.PlanningProblem):
                patch.append(patches.Rectangle(veh.initial_state.position[0]-3.5, veh.initial_state.position[1]-1.5, 7, 3, veh.initial_state.orientation ))
            else:
                draw_params = draw_params = {  'time_begin': time,
                                               'dynamic_obstacle':{'shape':{'facecolor': colors[group_ids[veh.obstacle_id]]}}}
                draw_object(veh, draw_params=draw_params)

        i = i + 1
    p = PatchCollection(patch)
    axes.add_collection(p)
    return None
