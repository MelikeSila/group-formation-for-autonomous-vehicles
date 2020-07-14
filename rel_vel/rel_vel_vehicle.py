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
    pos2is1 = [is1.position[0] + vx1, is1.position[1]+vy1]
    pos2is2=[is2.position[0]+ vx2, is2.position[1]+vy2]
  
    #calculate d2
    d2 = math.sqrt((pos2is2[0] - pos2is1[0]) ** 2 + (pos2is2[1] - pos2is1[1]) ** 2)

    #because we look at a step of one second, we can just subtract the positions from each other
    rel_vel = d2-d1

    return rel_vel
