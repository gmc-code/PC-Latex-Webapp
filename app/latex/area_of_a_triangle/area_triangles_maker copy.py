import zipfile
from pathlib import Path
from datetime import datetime
import pytz
import time
import random
from ..utilities.util_functions import merge_files, convert_to_pdf
from .area_of_a_triangle_functions import get_area_of_a_triangle_dict, get_side_pairs, get_rotations_shuffled


def make_diagram(tex_diagram_template_txt, tex_keys_q, process_dict):
    tex_diagram_template_txt_ans = tex_diagram_template_txt
    posttext = r"\vspace{1cm} \vfill"
    for key, value in process_dict.items():
        tex_diagram_template_txt_ans = tex_diagram_template_txt_ans.replace("<<" + key + ">>", value)
    for key, value in process_dict.items():
        if key in tex_keys_q:
            tex_diagram_template_txt = tex_diagram_template_txt.replace("<<" + key + ">>", value)
        else:
            tex_diagram_template_txt = tex_diagram_template_txt.replace("<<" + key + ">>", "\\dotuline{~~~~~~~}")  # non breaking spaces for gaps
    return tex_diagram_template_txt + posttext, tex_diagram_template_txt_ans + posttext


def generate_diagram_text(numq, triangle_type_num, process_func, diagram_template_texts_dict):
    # generate diagrams text and text for answers
    diagrams_text = ""
    diagrams_text_ans = ""
    # 4 to a page
    headtext = r"\pagebreak ~ \newline ~ \newline"
    for i in range(1, numq + 1):
        # pass in iteration number i
        img_tex, img_tex_ans = process_func(tex_diagram_template_txt_list[triangle_type_num], i)

        if i > 4 and i % 4 == 1:
            diagrams_text += headtext
            diagrams_text_ans += headtext
        diagrams_text += img_tex
        diagrams_text_ans += img_tex_ans
    return diagrams_text, diagrams_text_ans


def create_booklet(numq, triangle_type_num, title_text, process_func, tex_template_file, tex_ans_template_file, diagram_templates_dict, output_filename_prefix, file_type="pdf"):

    output_dir = Path(__file__).parent.parent.parent
    timestamp = "{date:%Y_%b_%d_%H_%M_%S}".format(date=datetime.now(tz=pytz.timezone("Australia/Melbourne")))
    currfile_dir_out = output_dir / "output"
    Path(currfile_dir_out).mkdir(parents=True, exist_ok=True)

    currfile_dir = Path(__file__).parent
    tex_template_path = currfile_dir / tex_template_file
    texans_template_path = currfile_dir / tex_ans_template_file
    diagram_template_paths_dict = {k: currfile_dir / v for k, v in diagram_templates_dict.items()}

    filename = f"{output_filename_prefix}_{timestamp}"

    tex_output_path = currfile_dir_out / f"{filename}_q.tex"
    tex_output_path_ans = currfile_dir_out / f"{filename}_ans.tex"
    tex_output_path_pdf = currfile_dir_out / f"{filename}_q.pdf"
    tex_output_path_ans_pdf = currfile_dir_out / f"{filename}_ans.pdf"
    tex_output_path_merged_pdf = currfile_dir_out / f"{filename}_merged.pdf"

    zip_output_path = currfile_dir_out / f"{filename}_files.zip"

    with open(tex_template_path, "r") as infile:
        tex_template_txt = infile.read()
    with open(texans_template_path, "r") as infile:
        tex_template_txt_ans = infile.read()
   # Read in the LaTeX diagram template file

    diagram_template_texts_dict = {}
    for key, path in diagram_template_paths_dict.items():
        with open(path, "r") as infile:
            diagram_template_texts_dict[key] = infile.read()
    # tex_diagram_right_template_txt,tex_diagram_acute_template_txt,tex_diagram_obtuse_template_txt


    # Use the function to generate diagram_text and diagram_text_ans
    diagram_text, diagram_text_ans = generate_diagram_text(numq, triangle_type_num, process_func, diagram_template_texts_dict)

    # Replace the <<title>> placeholder in the LaTeX template
    tex_template_txt = tex_template_txt.replace("<<title>>", title_text)
    tex_template_txt_ans = tex_template_txt_ans.replace("<<title>>", title_text)
    # Replace the <<diagrams>> placeholder in the LaTeX template
    tex_template_txt = tex_template_txt.replace("<<diagrams>>", diagram_text)
    tex_template_txt_ans = tex_template_txt_ans.replace("<<diagrams>>", diagram_text_ans)

    with open(tex_output_path, "w") as outfile:
        outfile.write(tex_template_txt)
    with open(tex_output_path_ans, "w") as outfile:
        outfile.write(tex_template_txt_ans)

    time.sleep(1)
    convert_to_pdf(tex_output_path, currfile_dir_out)
    convert_to_pdf(tex_output_path_ans, currfile_dir_out)
    merge_files(tex_output_path_pdf, tex_output_path_ans_pdf, tex_output_path_merged_pdf)

    if file_type == "zip":
        with zipfile.ZipFile(zip_output_path, "w") as zipf:
            zipf.write(tex_output_path_pdf, arcname=tex_output_path_pdf.name)
            zipf.write(tex_output_path_ans_pdf, arcname=tex_output_path_ans_pdf.name)
            zipf.write(tex_output_path_merged_pdf, arcname=tex_output_path_merged_pdf.name)
        return zip_output_path
    elif file_type == "pdf":
        return tex_output_path_merged_pdf
    else:
        raise ValueError("Invalid file type. Choose either 'pdf' or 'zip'.")


##############################################################################


def get_keys(num):
    tex_keys_q_right = ["calc_sidelength1", "calc_sidelength2", "sidelength1", "sidelength2", "rotation", "vA", "vB", "vC"]
    tex_keys_q_acute = ["calc_base", "calc_height", "leftoffset", "base", "height", "rotation", "vA", "vB", "vC", "vD"]
    tex_keys_q_obtuse = ["calc_base", "calc_height", "rightoffset", "base", "height", "rotation", "vA", "vB", "vC", "vD"]
    match num:
        case 1:
            return tex_keys_q_right
        case 2:
            return tex_keys_q_acute
        case 3:
            return tex_keys_q_obtuse

def get_kv(num,side_pair, rotation):
    return get_area_of_a_triangle_dict(num,side_pair, rotation)


def create_booklet_area_of_a_triangle(numq=20, triangle_type_num=4, file_type="pdf", show_dimension_lines_bool=True):
    # from webpage app


    # Generate shuffled lists of parameters
    side_pairs_list = get_side_pairs()
    rotations_list = get_rotations_shuffled()

    if show_dimension_lines_bool:
        # add in dl ones after testing
        diagram_templates = ["area_triangles_right_booklet_diagram_template.tex",
            "area_triangles_acute_booklet_diagram_template.tex",
            "area_triangles_obtuse_booklet_diagram_template.tex",]
    else:
        diagram_templates = ["area_triangles_right_booklet_diagram_template.tex",
            "area_triangles_acute_booklet_diagram_template.tex",
            "area_triangles_obtuse_booklet_diagram_template.tex",]

    diagram_templates_dict = {i + 1: name for i, name in enumerate(diagram_templates)}


    def make_diagram_wrapper(tex_diagram_template_txt, idx):
        # make_diagram_wrapper will be the process func that will be passed to create_booklet
        # within which generate_diagram_text uses the tex_diagram_template_txt parameter and gets the idx parameter from the repeat loop

        side_pair = side_pairs_list[idx - 1]
        rotation = rotations_list[idx - 1]

        if triangle_type_num == 4:
            tri_num = random.randint(1, 3)
        else:
            tri_num = triangle_type_num
        tex_keys_q = get_keys(tri_num)
        triangle_dict = get_kv(num_to_use, side_pair, rotation)

        return make_diagram(tex_diagram_template_txt, tri_num, tex_keys_q, triangle_dict)




    return create_booklet(
            numq,
            triangle_type_num,
            title_text,
            make_diagram_wrapper,
            "area_of_a_triangle_booklet_template.tex",
            "area_of_a_triangle_booklet_ans_template.tex",
            diagram_templates_dict,
            "areatri",
            file_type,
        )






