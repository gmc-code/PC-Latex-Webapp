from pathlib import Path
from datetime import datetime
import pytz
import time
from ..utilities.util_functions import merge_files, convert_to_pdf

#  python -m app.latex.numberlines.number_lines_maker_blank


def make_diagram_blank(tex_diagram_template_txt):
    posttext = r"\vspace{1pt}"
    return tex_diagram_template_txt + posttext


def generate_diagram_text_blank(numq, tex_diagram_template_txt):
    diagrams_text = ""
    # add the headtext
    headtext = r"\pagebreak ~ \newline ~ \newline"
    for i in range(1, numq + 1):
        img_tex = make_diagram_blank(tex_diagram_template_txt)
        if i > 8 and i % 8 == 1:
            diagrams_text += headtext
        diagrams_text += img_tex
    return diagrams_text


def create_booklet_blank(numq, title_text, tex_template_file, tex_diagram_template_file, output_filename_prefix):
    output_dir = Path(__file__).parent.parent.parent
    timestamp = "{date:%Y_%b_%d_%H_%M_%S}".format(date=datetime.now(tz=pytz.timezone("Australia/Melbourne")))
    currfile_dir_out = output_dir / "output"
    Path(currfile_dir_out).mkdir(parents=True, exist_ok=True)

    currfile_dir = Path(__file__).parent
    tex_template_path = currfile_dir / tex_template_file
    tex_diagram_template_path = currfile_dir / tex_diagram_template_file

    filename = f"{output_filename_prefix}_{timestamp}"

    tex_output_path = currfile_dir_out / f"{filename}.tex"
    tex_output_path_pdf = currfile_dir_out / f"{filename}.pdf"

    with open(tex_template_path, "r") as infile:
        tex_template_txt = infile.read()

    with open(tex_diagram_template_path, "r") as infile:
        tex_diagram_template_txt = infile.read()

    # Use the function to generate diagram_text and diagram_text_ans
    diagram_text = generate_diagram_text_blank(numq, tex_diagram_template_txt)

    tex_template_txt = tex_template_txt.replace("<<title>>", title_text)
    tex_template_txt = tex_template_txt.replace("<<diagrams>>", diagram_text)

    with open(tex_output_path, "w") as outfile:
        outfile.write(tex_template_txt)

    time.sleep(1)
    convert_to_pdf(tex_output_path, currfile_dir_out)
    return tex_output_path_pdf


def create_booklet_numberline_blank(numq=16, title_text="Number Lines"):
    return create_booklet_blank(
        numq,
        title_text,
        "number_lines_blank_booklet_template.tex",
        "number_lines_blank_booklet_diagram_template.tex",
        "nl_blank",
    )


def create_booklet_numberline_blank_0to20(numq=16, title_text="Number Lines +"):
    return create_booklet_blank(
        numq,
        title_text,
        "number_lines_blank_booklet_template.tex",
        "number_lines_0to20_blank_booklet_diagram_template.tex",
        "nl_blank_0to20",
    )


def create_booklet_numberline_blank_neg20to0(numq=16, title_text="Number Lines -"):
    return create_booklet_blank(
        numq,
        title_text,
        "number_lines_blank_booklet_template.tex",
        "number_lines_neg20to0_blank_booklet_diagram_template.tex",
        "nl_blank_neg20to0",
    )


# create_booklet_numberline_blank(numq=16)
# create_booklet_numberline_blank_neg20to0(numq=16)
