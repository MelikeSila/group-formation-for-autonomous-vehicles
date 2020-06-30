from commonroad.visualization.draw_dispatch_cr import draw_object
import commonroad.planning as planning
import matplotlib.patches as patches

def colorize_groups(group_assignment):
    colors=["'123456'", "'000000'", "'880000'", "'008800'", "'000088'", "'994499'", "'990022'". "'998822'"]
    i=0
    for group in group_assignment:

        draw_params = {'shape':{'facecolor':color}}
        for veh in group:
            if isinstance(veh, planning.planning_problem.PlanningProblem):
                rect=patches.Rectangle((veh.initial_state.position), 5, 2, veh.initial_state.orientation, linewidth=1, edgecolor=color, facecolor=color )

            else:
                draw_object(veh, draw_params=draw_params)

