import math


# function that uses two initial states as input to compute the relative velocity between them

def rel_vel_2_vehicles(is1, is2):
    # vel_x_direction_global_coordinate_system
    vx1 = math.cos(is1.orientation) * is1.velocity 
    vx2 = math.cos(is2.orientation) * is2.velocity 

    # vel_y_direction_global_coordinate_system
    vy1 = math.sin(is1.orientation) * is1.velocity
    vy2 = math.sin(is2.orientation) * is2.velocity

    # compute relative velocity
    # as we want to compute the relative velocity as derivative of the distance between them,
    # we calculate d1 as distance before and distance d2 as distance after one second of movement

    d1=math.sqrt((is2.position[0] - is1.position[0]) ** 2 + (is2.position[1] - is1.position[1]) ** 2)

    # calculate second position for both vehicles
    pos2is1 = [is1.position + [vx1, vy1]]
    pos2is2=[is2.position+[vx2, vy2]]
    # rel_vel = math.sqrt((vx2 - vx1) ** 2 + (vy2 - vy1) ** 2)

    return rel_vel
