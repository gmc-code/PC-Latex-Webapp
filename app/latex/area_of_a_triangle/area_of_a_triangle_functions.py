"""
Module of functions to return diagram dictionary for LaTeX
"""

import random


def get_area_of_a_triangle_dict(num,side_pair=None, rotation=None, show_dimension_lines_bool=True, show_vertices_bool=True,  allow_rotation_bool=True, units="Random"):
    match num:
        case 1:
            return get_area_of_a_triangle_right_dict(side_pair, rotation, show_dimension_lines_bool, show_vertices_bool, allow_rotation_bool, units)
        case 2:
            return get_area_of_a_triangle_acute_dict(side_pair, rotation, show_dimension_lines_bool, show_vertices_bool, allow_rotation_bool, units)
        case 3:
            return get_area_of_a_triangle_obtuse_dict(side_pair, rotation,show_dimension_lines_bool, show_vertices_bool, allow_rotation_bool, units)



def get_side_pairs():
    # 28 pairs
    pairs = [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 4),
             (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 5), (4, 6), (4, 7),
             (4, 8), (4, 9), (5, 6), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8),
             (6, 9), (7, 8), (7, 9), (8, 9)]
    random.shuffle(pairs)
    return pairs


def get_rotations_shuffled():
    # Define the range of angles with weighting for 0
    # angles = [0, 0, 0, 0, 0, 10, 20, 30, -10, -20, -30] + [90, 90, 90, 90, 90, 100, 110, 120, 80, 70, 60] + [180, 180, 180, 180, 180, 190, 200, 210, 170, 160, 150] + [270, 270, 270, 270, 270, 280, 290, 300, 260, 250, 240]
    angles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 20, 30, -10, -20, -30] + [90, 60, 120] + [180, 150, 210] + [240, 270]
    # angles = [0] * 20
    # Shuffle list
    random.shuffle(angles)
    return angles


def get_random_units():
    return random.choice(["mm", "cm", "m", "km"])


def get_area_of_a_triangle_right_dict(side_pair=None, rotation=None, show_dimension_lines_bool=True, allow_rotation_bool=True, units="Random"):
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


    calc_base = side_pair[1]  # longer
    calc_height = side_pair[0]  # shorter
    height = round(random.uniform(0, 1.0) + 1.5, 3)
    base = round(height * (calc_base / calc_height), 3)

    if base > 7:
        ratio = 7 / base
        base = round(base * ratio, 3)
        height = round(height * ratio, 3)

    calc_area_value = 0.5 * calc_base * calc_height
    calc_formula_part1 = r"\frac{1}{2}"
    calc_formula_part2 = "^2"

    # gap_to_fill = "\\dotuline{~~~~~~~}"

    vertices_lists = [["A", "B", "C"], ["E", "F", "G"], ["K", "L", "M"],
                      ["R", "S", "T"], ["X", "Y", "Z"]]

    vertices_labels = random.choice(vertices_lists)

    # random.shuffle(vertices_labels)
    # vertexA
    vA = vertices_labels[0]
    vB = vertices_labels[1]
    vC = vertices_labels[2]

    kv = dict()

    kv["calc_base"] = f"{calc_base}"
    kv["calc_height"] = f"{calc_height}"
    kv["base"] = f"{base}"
    kv["height"] = f"{height}"
    kv["rotation"] = f"{rotation}"
    kv["units"] = f"{units}"
    kv["calc_units"] = f"{units}"
    kv["calc_formula_part1"] = f"{calc_formula_part1}"
    kv["calc_formula_part2"] = f"{calc_formula_part2}"

    kv["vA"] = f"{vA}"
    kv["vB"] = f"{vB}"
    kv["vC"] = f"{vC}"

    kv["calc_base_value"] = f"{calc_base}"
    kv["calc_height_value"] = f"{calc_height}"
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




def get_area_of_a_triangle_acute_dict(side_pair=None, rotation=None, show_dimension_lines_bool=True, allow_rotation_bool=True, units="Random"):
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

    calc_base = side_pair[1] # longer
    calc_height = side_pair[0] # shorter
    height = round(random.uniform(0, 1.0) + 1.5, 3)
    base = round(height * (calc_base / calc_height), 3)

    if base > 7:
        ratio = 7 / base
        base = round(base * ratio, 3)
        height = round(height * ratio, 3)

    leftoffset = round(random.uniform(0, base - 1) + 0.5, 3)
    calc_area_value = 0.5 * calc_base * calc_height
    calc_formula_part1 = r"\frac{1}{2}"
    calc_formula_part2 = "^2"

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

    kv["calc_base"] = f"{calc_base}"
    kv["calc_height"] = f"{calc_height}"
    kv["base"] = f"{base}"
    kv["height"] = f"{height}"
    kv["leftoffset"] = f"{leftoffset}"
    kv["rotation"] = f"{rotation}"
    kv["units"] = f"{units}"
    kv["calc_units"] = f"{units}"
    kv["calc_formula_part1"] = f"{calc_formula_part1}"
    kv["calc_formula_part2"] = f"{calc_formula_part2}"

    kv["vA"] = f"{vA}"
    kv["vB"] = f"{vB}"
    kv["vC"] = f"{vC}"
    kv["vD"] = f"{vD}"

    kv["calc_base_value"] = f"{calc_base}"
    kv["calc_height_value"] = f"{calc_height}"
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



def get_area_of_a_triangle_obtuse_dict(side_pair=None, rotation=None, show_dimension_lines_bool=True,  show_vertices_bool=True, allow_rotation_bool=True, units="Random"):
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

    calc_base = side_pair[1]  # longer
    calc_height = side_pair[0]  # shorter
    height = round(random.uniform(0, 1.0) + 1.5, 3)
    base = round(height * (calc_base / calc_height), 3)
    rightoffset = round(random.uniform(0, 1) + 0.5, 3)

    if base + rightoffset > 7:
        ratio = 7 / (base + rightoffset)
        base = round(base * ratio, 3)
        rightoffset = round(rightoffset * ratio, 3)
        height = round(height * ratio, 3)

    calc_area_value = 0.5 * calc_base * calc_height
    calc_formula_part1 = r"\frac{1}{2}"
    calc_formula_part2 = "^2"

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

    kv["calc_base"] = f"{calc_base}"
    kv["calc_height"] = f"{calc_height}"
    kv["base"] = f"{base}"
    kv["height"] = f"{height}"
    kv["rightoffset"] = f"{rightoffset}"
    kv["rotation"] = f"{rotation}"
    kv["units"] = f"{units}"
    kv["calc_units"] = f"{units}"
    kv["calc_formula_part1"] = f"{calc_formula_part1}"
    kv["calc_formula_part2"] = f"{calc_formula_part2}"

    kv["vA"] = f"{vA}"
    kv["vB"] = f"{vB}"
    kv["vC"] = f"{vC}"
    kv["vD"] = f"{vD}"

    kv["calc_base_value"] = f"{calc_base}"
    kv["calc_height_value"] = f"{calc_height}"
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
