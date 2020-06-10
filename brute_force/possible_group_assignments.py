def all_group_assignments(veh_list):
    # iterates through all possible group sizes as k_partitions only generates the outcome for one number of groups
    groups_assignments = []
    for l in range(1,len(veh_list)+1):
        groups_assignments.append(k_partitions(veh_list, l))
    assignments =[]

    for x in groups_assignments:
        assignments +=x
    return assignments

def k_partitions(seq, k):
    """Returns a list of all unique k-partitions of `seq`.

    Each partition is a list of parts, and each part is a tuple.


    """
    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()

            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    result = generate_partitions(0)

    return result