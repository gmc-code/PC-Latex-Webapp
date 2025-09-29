import zipfile
import random
import time
from pathlib import Path
from datetime import datetime
import pytz

from ..utilities.util_functions import merge_files, convert_to_pdf
from .area_of_a_triangle_functions import get_area_of_a_triangle_dict, get_side_pairs, get_rotations_shuffled


def make_diagram(tex_diagram_template_txt, tex_keys_q, process_dict):
    tex_diagram_template_txt_ans = tex_diagram_template_txt
    posttext = r"\vspace{1cm} \vfill"

    for key, value in process_dict.items():
        tex_diagram_template_txt_ans = tex_diagram_template_txt_ans.replace(f"<<{key}>>", value)
        replacement = value if key in tex_keys_q else r"\dotuline{~~~~~~~}"
        tex_diagram_template_txt = tex_diagram_template_txt.replace(f"<<{key}>>", replacement)

    return tex_diagram_template_txt + posttext, tex_diagram_template_txt_ans + posttext


def generate_diagram_text(numq, process_func):
    diagrams_text = ""
    diagrams_text_ans = ""
    headtext = r"\pagebreak ~ \newline ~ \newline"

    for i in range(1, numq + 1):
        img_tex, img_tex_ans = process_func(i)

        if i > 4 and i % 4 == 1:
            diagrams_text += headtext
            diagrams_text_ans += headtext

        diagrams_text += img_tex
        diagrams_text_ans += img_tex_ans

    return diagrams_text, diagrams_text_ans


def create_booklet(numq, title_text, process_func, tex_template_file, tex_ans_template_file, output_filename_prefix, file_type="pdf"):
    output_dir = Path(__file__).parent.parent.parent
    currfile_dir = Path(__file__).parent
    timestamp = datetime.now(tz=pytz.timezone("Australia/Melbourne")).strftime("%Y_%b_%d_%H_%M_%S")
    currfile_dir_out = output_dir / "output"
    currfile_dir_out.mkdir(parents=True, exist_ok=True)

    filename = f"{output_filename_prefix}_{timestamp}"

    tex_output_path = currfile_dir_out / f"{filename}_q.tex"
    tex_output_path_ans = currfile_dir_out / f"{filename}_ans.tex"
    tex_output_path_pdf = currfile_dir_out / f"{filename}_q.pdf"
    tex_output_path_ans_pdf = currfile_dir_out / f"{filename}_ans.pdf"
    tex_output_path_merged_pdf = currfile_dir_out / f"{filename}_merged.pdf"
    zip_output_path = currfile_dir_out / f"{filename}_files.zip"

    tex_template_txt = (currfile_dir / tex_template_file).read_text()
    tex_template_txt_ans = (currfile_dir / tex_ans_template_file).read_text()

    diagram_text, diagram_text_ans = generate_diagram_text(numq, process_func)

    tex_template_txt = tex_template_txt.replace("<<title>>", title_text).replace("<<diagrams>>", diagram_text)
    tex_template_txt_ans = tex_template_txt_ans.replace("<<title>>", title_text).replace("<<diagrams>>", diagram_text_ans)

    tex_output_path.write_text(tex_template_txt)
    tex_output_path_ans.write_text(tex_template_txt_ans)

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


def get_keys(num):
    tex_keys_q_right = ['draw_style', "calc_sidelength1", "calc_sidelength2", "sidelength1", "sidelength2", "rotation", "vA", "vB", "vC"]
    tex_keys_q_acute = ['draw_style', "calc_base", "calc_height", "leftoffset", "base", "height", "rotation", "vA", "vB", "vC", "vD"]
    tex_keys_q_obtuse = ['draw_style', "calc_base", "calc_height", "rightoffset", "base", "height", "rotation", "vA", "vB", "vC", "vD"]

    match num:
        case 1:
            return tex_keys_q_right
        case 2:
            return tex_keys_q_acute
        case 3:
            return tex_keys_q_obtuse


def get_kv(num, side_pair, rotation, show_dimension_lines_bool):
    return get_area_of_a_triangle_dict(num, side_pair, rotation, show_dimension_lines_bool)




def create_booklet_area_of_a_triangle(numq=20, triangle_type_num=4, title_text="Area of a Triangle",file_type="pdf", show_dimension_lines_bool=True):
    title_text = "Area of a Triangle"
    side_pairs_list = get_side_pairs()
    rotations_list = get_rotations_shuffled()
    diagram_templates = ["area_of_a_triangle_right_booklet_diagram_template.tex",
            "area_of_a_triangle_acute_booklet_diagram_template.tex",
            "area_of_a_triangle_obtuse_booklet_diagram_template.tex",]

    diagram_templates_dict = {i + 1: name for i, name in enumerate(diagram_templates)}
    # Load diagram templates once and share with inner function
    currfile_dir = Path(__file__).parent
    diagram_template_paths_dict = {k: currfile_dir / v for k, v in diagram_templates_dict.items()}
    diagram_template_texts_dict = {k: path.read_text() for k, path in diagram_template_paths_dict.items()}

    def make_diagram_wrapper(idx):
        side_pair = side_pairs_list[idx - 1]
        rotation = rotations_list[idx - 1]
        tri_num = random.randint(1, 3) if triangle_type_num == 4 else triangle_type_num

        tex_keys_q = get_keys(tri_num)
        triangle_dict = get_kv(tri_num, side_pair, rotation, show_dimension_lines_bool)
        tex_diagram_template_txt = diagram_template_texts_dict[tri_num]

        return make_diagram(tex_diagram_template_txt, tex_keys_q, triangle_dict)


    return create_booklet(
        numq,
        title_text,
        make_diagram_wrapper,
        "area_of_a_triangle_booklet_template.tex",
        "area_of_a_triangle_booklet_ans_template.tex",
        "areatri",
        file_type,
    )
