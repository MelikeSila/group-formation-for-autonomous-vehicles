from commonroad.visualization.draw_dispatch_cr import draw_object
import commonroad.planning as planning
import matplotlib.patches as patches


def colorize_groups(group_assignment, axes):
    colors = ['#123456', '#000000', '#880000', '#008800', '#000088', '#994499', '#990022', '#998822']
    i,j = 0,0
    rect = []
    for group in group_assignment:
        color = colors[i % 8]
        draw_params = {'shape': {'facecolor': color}}
        for veh in group:
            if isinstance(veh, planning.planning_problem.PlanningProblem):
                rect[j] = patches.Rectangle((veh.initial_state.position), 7, 3, veh.initial_state.orientation,
                                            linewidth=1, edgecolor=color, facecolor=color)
                j = j + 1

            else:
                draw_object(veh, draw_params=draw_params)

        i = i + 1
    axes.add_patch(rect)
    return None
