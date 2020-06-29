import GraphBasedDistanceMeasure

def group_dist(scenario, objects):


    group_size = len(objects)

    # loop sum graph-based distance measure
    sum_dist = 0
    for i in range(0, group_size):
        for j in range(i, group_size):

            sum_dist = sum_dist + GraphBasedDistanceMeasure.D(objects[i], objects[j])

    # normalize sum_dist with group size
    if group_size == 1:
        sum_dist = sum_dist
    else:
        sum_dist = sum_dist / (group_size * (group_size - 1))

    return sum_dist
