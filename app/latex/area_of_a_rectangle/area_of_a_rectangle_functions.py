"""
Module of functions to return diagram dictionary for LaTeX
"""

import random


def get_side_pairs():
    pairs = [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 5),
             (4, 6), (4, 7), (4, 8), (4, 9), (5, 6), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9)]
    random.shuffle(pairs)
    return pairs


def get_rotations_shuffled():
    # Define the range of angles with weighting for 0
    angles = [0, 0, 0, 0, 0, 10, 20, 30, -10, -20, -30] * 2
    # Shuffle list
    random.shuffle(angles)
    return angles


def get_random_units():
    return random.choice(["mm", "cm", "m", "km"])



def get_area_of_a_rectangle_dict(side_pair=None, rotation=None, show_dimension_lines_bool=True,  show_vertices_bool=True, allow_rotation_bool=True, units="Random"):
    # 1 longer than 2 and to scale
    if side_pair is None:
        side_pair = get_side_pairs()[0]
    if rotation is None:
        rotation = get_rotations_shuffled()[0]
    if allow_rotation_bool is False:
        # remove rotation by setting to 0
        rotation = 0
    if units == "Random":
        units = get_random_units()


    calc_sidelength1 = side_pair[1]  #longer
    calc_sidelength2 = side_pair[0]  # shorter
    sidelength2 = round(random.uniform(0, 1.0) + 1.5, 3)
    sidelength1 = round(sidelength2 * (calc_sidelength1 / calc_sidelength2), 3)

    if sidelength1 > 8:
        ratio = 8 / sidelength1
        sidelength1 = round(sidelength1 * ratio, 3)
        sidelength2 = round(sidelength2 * ratio, 3)

    calc_area_value = calc_sidelength1 * calc_sidelength2
    calc_formula_part1 = "^2"

    # gap_to_fill = "\\dotuline{~~~~~~~}"

    vertices_lists = [["A", "B", "C", "D"], ["E", "F", "G", "H"],
                      ["K", "L", "M", "N"], ["Q", "R", "S", "T"],
                      ["W", "X", "Y", "Z"]]
    vertices_labels = random.choice(vertices_lists)

    # random.shuffle(vertices_labels)
    # vertexA
    vA = vertices_labels[0]
    vB = vertices_labels[1]
    vC = vertices_labels[2]
    vD = vertices_labels[3]

    kv = dict()

    kv["calc_sidelength1"] = f"{calc_sidelength1}"
    kv["calc_sidelength2"] = f"{calc_sidelength2}"
    kv["sidelength1"] = f"{sidelength1}"
    kv["sidelength2"] = f"{sidelength2}"
    kv["rotation"] = f"{rotation}"
    kv["units"] = f"{units}"
    kv["calc_units"] = f"{units}"
    kv["calc_formula_part1"] = f"{calc_formula_part1}"

    kv["vA"] = f"{vA}"
    kv["vB"] = f"{vB}"
    kv["vC"] = f"{vC}"
    kv["vD"] = f"{vD}"

    kv["calcside_value1"] = f"{calc_sidelength1}"
    kv["calcside_value2"] = f"{calc_sidelength2}"
    kv["calc_area_value"] = f"{calc_area_value}"

    if show_dimension_lines_bool is True:
        kv["draw_style"] = "<->, gray"
    else:
        kv["draw_style"] = "draw=none"

    if show_vertices_bool is True:
        kv["show_vertices"] = r"\ifTrue"
    else:
        kv["show_vertices"] = r"\ifFalse"

    return kv
