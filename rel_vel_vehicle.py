import math


# function that uses two initial states as input to compute the relative velocity between them

def rel_vel_2_vehicles(is1, is2):
    # vel_x_direction_global_coordinate_system
    vx1 = math.cos(is1.orientation) * is1.velocity - math.sin(is1.orientation) * is1.velocity_y
    vx2 = math.cos(is2.orientation) * is2.velocity - math.sin(is2.orientation) * is2.velocity_y

    # vel_y_direction_global_coordinate_system
    vy1 = math.cos(is1.orientation) * is1.velocity_y + math.sin(is1.orientation) * is1.velocity
    vy2 = math.cos(is2.orientation) * is2.velocity_y + math.sin(is2.orientation) * is2.velocity

    # compute relative velocity

    rel_vel = math.sqrt((vx2 - vx1) ** 2 + (vy2 - vy1) ** 2)
    return rel_vel
