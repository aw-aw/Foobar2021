import random


def thumbWarBrute(a_count, b_count):
    previous = []
    while True:
        if a_count == b_count:
            return 2
        if a_count < b_count:
            b_temp = b_count - a_count
            a_temp = 2 * a_count
        else:
            a_temp = a_count - b_count
            b_temp = 2 * b_count
        next = sorted([a_temp, b_temp])
        if next in previous:
            return 0
        previous.append(next)
        a_count = a_temp
        b_count = b_temp  # this is the traditional algorithm


def overlap(pair1, pair2):
    for i in range(2):
        for j in range(2):
            if pair1[i] == pair2[j]:
                return True
    return False


def generateOverlapDict(infinite_set):
    overlap_dict = {}
    temp_dict = {}
    for i in range(len(infinite_set)):
        pair = infinite_set[i]
        for item in pair:
            if item not in temp_dict.keys():
                temp_dict[item] = [i]
            else:
                temp_dict[item].append(i)
    for i in range(len(infinite_set)):
        pair = infinite_set[i]
        overlaps = []
        for item in pair:
            for match in temp_dict[item]:
                if match != i:
                    overlaps.append(match)
        overlaps.sort()
        overlap_dict[i] = overlaps
    return overlap_dict


def thumbWar(a_count, b_count):
    diff = abs(a_count - b_count)
    if diff % 2 == 1:
        return 0
    val = int((a_count + b_count) / 2)
    if (val & (val-1) == 0):
        return 2
    else:
        while val % 2 == 0:
            val = int(val / 2)
        if diff % val == 0:
            return 2
        return 0


def solution(banana_list):
    max_pairs = int(len(banana_list) / 2)
    infinite_set = []
    for i in range(len(banana_list)):
        for j in range(i, len(banana_list)):
            res = thumbWar(banana_list[i], banana_list[j])
            if res == 0:
                infinite_set.append([i, j])
    while len(infinite_set) > 0:
        overlap_dict = generateOverlapDict(infinite_set)
        max_pairs -= 1
        keys = list(overlap_dict.keys())
        vals = list(overlap_dict.values())
        sorted_vals = sorted(vals, key=len)
        least_overlap_vals = sorted_vals[0]
        pos = vals.index(least_overlap_vals)
        least_overlap_key = [keys[pos]]
        least_overlaps = least_overlap_key + least_overlap_vals
        infinite_set = [i for j, i in enumerate(infinite_set) if j not in least_overlaps]
    max_pairs *= 2
    max_pairs += (len(banana_list) % 2)
    return max_pairs


def guardSet(max_guard, max_val):
    out = []
    for i in range(max_guard):
        out.append(random.randrange(1, max_val))
    return out


print(solution([1, 7, 3, 21, 13, 19]))
