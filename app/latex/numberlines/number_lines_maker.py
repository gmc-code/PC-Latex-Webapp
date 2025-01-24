import zipfile
from pathlib import Path
from datetime import datetime
import pytz
import time
from ..utilities.util_functions import merge_files, convert_to_pdf
from .number_lines_functions import getprocess_dict

#  python -m app.latex.numberlines.number_lines_maker


kv_keys_ans = ["startval", "endval", "startvaltxt", "endvaltxt", "changevaltxt", "equtxt"]
kv_keys_q = ["startval", "endval", "startvaltxt_q", "endvaltxt_q", "changevaltxt_q", "equtxt_q"]


def trimkey(key):
    key = key.replace("_q", "")
    return key


def make_diagram(tex_diagram_template_txt, process_dict):
    posttext = r"\vspace{-2pt}"
    tex_diagram_template_txt_ans = tex_diagram_template_txt
    for key, value in process_dict.items():
        # show answers
        if key in kv_keys_ans:
            tex_diagram_template_txt_ans = tex_diagram_template_txt_ans.replace("<<" + key + ">>", value)
    for key, value in process_dict.items():
        # don't show answers, use ___ for gaps
        if key in kv_keys_q:
            tex_diagram_template_txt = tex_diagram_template_txt.replace("<<" + trimkey(key) + ">>", value)
    return tex_diagram_template_txt + posttext, tex_diagram_template_txt_ans + posttext


def generate_diagram_text(numq, process_func, tex_diagram_template_txt):
    # generate diagrams text and text for answers
    diagrams_text = ""
    diagrams_text_ans = ""
    # add the headtext
    headtext = r"\pagebreak ~ \newline ~ \newline"
    for i in range(1, numq + 1):
        img_tex, img_tex_ans = process_func(tex_diagram_template_txt)
        if i > 8 and i % 8 == 1:
            diagrams_text += headtext
            diagrams_text_ans += headtext
        diagrams_text += img_tex
        diagrams_text_ans += img_tex_ans
    return diagrams_text, diagrams_text_ans


def create_booklet(numq, title_text, process_func, tex_template_file, tex_ans_template_file, tex_diagram_template_file, output_filename_prefix, file_type="pdf"):

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

def create_booklet_numberline(numq=16, num=6, title_text="Number Lines", file_type="pdf"):

    def make_diagram_wrapper(tex_diagram_template_txt):
        return make_diagram(tex_diagram_template_txt, getprocess_dict(num, adjustment=0))

    return create_booklet(
        numq,
        title_text,
        make_diagram_wrapper,
        "number_lines_booklet_template.tex",
        "number_lines_booklet_ans_template.tex",
        "number_lines_booklet_diagram_template.tex",
        "nl",
        file_type,
    )


def create_booklet_numberline_0to20(numq=16, num=6, title_text="Number Lines +", file_type="pdf"):

    def make_diagram_wrapper(tex_diagram_template_txt):
        return make_diagram(tex_diagram_template_txt, getprocess_dict(num, adjustment=10))

    return create_booklet(
        numq,
        title_text,
        make_diagram_wrapper,
        "number_lines_booklet_template.tex",
        "number_lines_booklet_ans_template.tex",
        "number_lines_0to20_booklet_diagram_template.tex",
        "nl_0to20",
        file_type,
    )


def create_booklet_numberline_neg20to0(numq=16, num=6, title_text="Number Lines -", file_type="pdf"):

    def make_diagram_wrapper(tex_diagram_template_txt):
        return make_diagram(tex_diagram_template_txt, getprocess_dict(num, adjustment=-10))

    return create_booklet(
        numq,
        title_text,
        make_diagram_wrapper,
        "number_lines_booklet_template.tex",
        "number_lines_booklet_ans_template.tex",
        "number_lines_neg20to0_booklet_diagram_template.tex",
        "nl_neg20to0",
        file_type,
    )


# create_booklet_numberline(numq=16, num=6, file_type="pdf")
