"""
Module of functions to return diagram dictionary for LaTeX
"""

import random


def get_ints_shuffled_one_dig_first():
    # Define the range of integers
    numbers1 = list(range(1, 10))
    numbers2 = list(range(10, 21))
    # Shuffle each list
    random.shuffle(numbers1)
    random.shuffle(numbers2)
    # Join the two lists
    numbers = numbers1 + numbers2
    return numbers


def get_rotations_shuffled():
    # Define the range of angles with weighting for 0
    angles = [0, 0, 0, 0, 0, 10, 20, 30, -10, -20, -30] * 2
    # Shuffle list
    random.shuffle(angles)
    return angles


def get_random_units():
    return random.choice(["mm", "cm", "m", "km"])


def get_perimeter_of_a_square_dict(side_int=None, rotation=None, show_dimension_lines_bool=True, show_vertices_bool=True, allow_rotation_bool=True, units="cm"):
    if side_int is None:
        side_int = get_ints_shuffled_one_dig_first()[0]
    if rotation is None:
        rotation = get_rotations_shuffled()[0]
    if allow_rotation_bool is False:
        # remove rotation by setting to 0
        rotation = 0
    if units == "Random":
        units = get_random_units()

    calc_sidelength = side_int
    sidelength = round(random.uniform(0, 1.5) + 1.5, 3)
    calc_perimeter_value = 4 * calc_sidelength
    calc_formula_part1 = "4"

    # gap_to_fill = "\\dotuline{~~~~~~~}"

    vertices_lists = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["K", "L", "M", "N"], ["Q", "R", "S", "T"], ["W", "X", "Y", "Z"]]
    vertices_labels = random.choice(vertices_lists)

    # random.shuffle(vertices_labels)
    # vertexA
    vA = vertices_labels[0]
    vB = vertices_labels[1]
    vC = vertices_labels[2]
    vD = vertices_labels[3]

    kv = dict()

    kv["calc_sidelength"] = f"{calc_sidelength}"
    kv["sidelength"] = f"{sidelength}"
    kv["rotation"] = f"{rotation}"
    kv["units"] = f"{units}"
    kv["calc_units"] = f"{units}"
    kv["calc_formula_part1"] = f"{calc_formula_part1}"

    kv["vA"] = f"{vA}"
    kv["vB"] = f"{vB}"
    kv["vC"] = f"{vC}"
    kv["vD"] = f"{vD}"

    kv["calcside_value"] = f"{calc_sidelength}"
    kv["calc_perimeter_value"] = f"{calc_perimeter_value}"

    if show_dimension_lines_bool is True:
        kv["draw_style"] = "<->, gray"
    else:
        kv["draw_style"] = "draw=none"

    if show_vertices_bool is True:
        kv["show_vertices"] = r"\ifTrue"
    else:
        kv["show_vertices"] = r"\ifFalse"

    return kv
