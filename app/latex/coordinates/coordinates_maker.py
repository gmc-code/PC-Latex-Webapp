import zipfile
from pathlib import Path
from datetime import datetime
import pytz
import time
from ..utilities.util_functions import merge_files, convert_to_pdf
from .coordinates_functions import get_coordinates_dict


kv_keys_q = ["points_to_list"]
kv_keys_ans = ["points_to_list", "points_to_plot"]
ky_keys_to_clear = ["points_to_plot"]


def make_diagram(tex_diagram_template_txt, process_dict):
    tex_diagram_template_txt_ans = tex_diagram_template_txt
    for key, value in process_dict.items():
        # show answers
        if key in kv_keys_ans:
            tex_diagram_template_txt_ans = tex_diagram_template_txt_ans.replace(
                "<<" + key + ">>", value)
    for key, value in process_dict.items():
        # don't show answers
        if key in kv_keys_q:
            tex_diagram_template_txt = tex_diagram_template_txt.replace(
                "<<" + key + ">>", value)

        if key in ky_keys_to_clear:
            tex_diagram_template_txt = tex_diagram_template_txt.replace(
                "<<" + key + ">>", "")
    return tex_diagram_template_txt, tex_diagram_template_txt_ans


def generate_diagram_text(numq, process_func, tex_diagram_template_txt):
    # generate diagrams text and text for answers
    diagrams_text = ""
    diagrams_text_ans = ""
    headtext_page = r"\pagebreak ~ \newline ~ \newline"
    #
    for i in range(1, numq + 1):
        img_tex, img_tex_ans = process_func(tex_diagram_template_txt)
        diagrams_text += img_tex
        diagrams_text_ans += img_tex_ans
        if i < numq:
            diagrams_text += headtext_page
            diagrams_text_ans += headtext_page
    return diagrams_text, diagrams_text_ans



def create_booklet_coordinates(numq, title_text, process_func, tex_template_file, tex_ans_template_file, tex_diagram_template_file, output_filename_prefix, file_type="pdf"):
    output_dir = Path(__file__).parent.parent.parent
    timestamp = "{date:%Y_%b_%d_%H_%M_%S}".format(date=datetime.now(tz=pytz.timezone("Australia/Melbourne")))
    currfile_dir_out = output_dir / "output"
    Path(currfile_dir_out).mkdir(parents=True, exist_ok=True)

    currfile_dir = Path(__file__).parent
    tex_template_path = currfile_dir / tex_template_file
    texans_template_path = currfile_dir / tex_ans_template_file
    tex_diagram_template_path = currfile_dir / tex_diagram_template_file

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
    with open(tex_diagram_template_path, "r") as infile:
        tex_diagram_template_txt = infile.read()

    # Use the function to generate diagram_text and diagram_text_ans
    diagram_text, diagram_text_ans = generate_diagram_text(numq, process_func, tex_diagram_template_txt)

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



def create_booklet_coords(numq=2, title_text="Coordinates",  num_points=10, file_type="pdf"):

    def make_diagram_wrapper(tex_diagram_template_txt):
        return make_diagram(tex_diagram_template_txt, get_coordinates_dict(num_points))

    return create_booklet_coordinates(
        numq,
        title_text,
        make_diagram_wrapper,
        "coordinates_booklet_template.tex",
        "coordinates_booklet_ans_template.tex",
        "coordinates_booklet_diagram_template.tex",
        "coords",
        file_type,
    )


