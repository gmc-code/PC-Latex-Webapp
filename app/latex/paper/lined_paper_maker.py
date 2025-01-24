from pathlib import Path
from datetime import datetime
import pytz
import time
from ..utilities.util_functions import merge_files, convert_to_pdf
from . import lined_paper_functions as lpf

#####################################################################################


def create_lines(num, whole_page_bool, tex_template_file, output_filename_prefix):
    output_dir = Path(__file__).parent.parent.parent
    timestamp = "{date:%Y_%b_%d_%H_%M_%S}".format(date=datetime.now(tz=pytz.timezone("Australia/Melbourne")))
    currfile_dir_out = output_dir / "output"
    Path(currfile_dir_out).mkdir(parents=True, exist_ok=True)

    currfile_dir = Path(__file__).parent
    tex_template_path = currfile_dir / tex_template_file

    filename = f"{output_filename_prefix}_{timestamp}"

    tex_output_path = currfile_dir_out / f"{filename}.tex"
    tex_output_path_pdf = currfile_dir_out / f"{filename}.pdf"

    # Read in the LaTeX template file
    with open(tex_template_path, "r") as infile:
        tex_template_txt = infile.read()

    # <<diagrams>>
    if whole_page_bool:
        # full page
        diagrams_text = lpf.get_lined_page_diagram(num)
        # Replace the <<diagrams>> placeholder in the LaTeX template with the generated diagrams
        tex_template_txt = tex_template_txt.replace("<<diagrams>>", diagrams_text)
    else:
        diagrams_text = lpf.get_lined_paper_diagram(num)
        # Replace the <<diagrams>> placeholder in the LaTeX template with the generated diagrams
        tex_template_txt = tex_template_txt.replace("<<diagrams>>", diagrams_text)
        #
        paperheight = lpf.get_lined_paper_height(num)
        # Replace the <<diagrams>> placeholder in the LaTeX template with the generated diagrams
        tex_template_txt = tex_template_txt.replace("<<paperheight>>", paperheight)

    # Write the question tex to an output file
    with open(tex_output_path, "w") as outfile:
        outfile.write(tex_template_txt)

    time.sleep(1)
    convert_to_pdf(tex_output_path, currfile_dir_out)
    return tex_output_path_pdf


def create_lined_paper(num=4):
    return create_lines(
        num,
        False,
        "lined_paper_template.tex",
        "lines",
    )

def create_lined_page(num=26):
    return create_lines(
        num,
        True,
        "lined_page_template.tex",
        "lined_page",
    )
