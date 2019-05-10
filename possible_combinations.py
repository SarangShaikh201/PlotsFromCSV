import itertools
import copy

def get_all_columns_combinations(column_names):
    possible_combs = []

    """Getting all possible combinations"""

    for i in range(2, len(column_names) + 1):
        possible_combs.append(list(itertools.combinations(column_names, i)))

    """Spliiting the combinations in two pieces"""

    combs = []
    total_combs = 0
    for comb in possible_combs[0]:
        combs.append([[comb[0]], [comb[1]]])
        total_combs += 1

    for level_no, level in enumerate(possible_combs[1:]):
        for combination in level:
            for internal_split_val in range(2, level_no + 3):
                for internal_possible_comb in (list(itertools.combinations(combination, internal_split_val))):
                    combs.append([list(internal_possible_comb), []])
                    for column in combination:
                        if column not in internal_possible_comb:
                            combs[total_combs][1].append(column)
                    total_combs += 1

    temp_comb = copy.copy(combs)
    for item in temp_comb:
        temp = [item[1], item[0]]
        combs.append(temp)

    return combs
