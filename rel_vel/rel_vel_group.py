from . import rel_vel_vehicle


def calc_rel_vel_group(state_list):
    # get group size
    group_size = len(state_list)

    # loop sum relative velocities wihtin a group according to Frese, Beyerer, Zimmer
    sum_rel_vel = 0
    for i in range(0, group_size):
        for j in range(i, group_size):
            sum_rel_vel = sum_rel_vel + rel_vel_vehicle.rel_vel_2_vehicles(state_list[i], state_list[j])

    # normalize relative velocity with group size
    rel_vel_group = sum_rel_vel / (group_size * (group_size - 1))

    return rel_vel_group
