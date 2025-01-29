from pathlib import Path
from datetime import datetime
import pytz
import time
from ..utilities.util_functions import merge_files, convert_to_pdf


#####################################################################################


def create_gridpaper_std_file(paperheight, paperwidth, patternsize, majorcolor, minorcolor, tex_template_file, output_filename_prefix):
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


    # Replace the placeholders in the LaTeX template
    # paperheight, paperwidth, patternsize, minorcolor,
    tex_template_txt = tex_template_txt.replace("<<paperheight>>", paperheight)
    tex_template_txt = tex_template_txt.replace("<<paperwidth>>", paperwidth)
    tex_template_txt = tex_template_txt.replace("<<patternsize>>", patternsize)
    tex_template_txt = tex_template_txt.replace("<<majorcolor>>", majorcolor)
    tex_template_txt = tex_template_txt.replace("<<minorcolor>>", minorcolor)

    # Write the question tex to an output file
    with open(tex_output_path, "w") as outfile:
        outfile.write(tex_template_txt)

    time.sleep(1)
    convert_to_pdf(tex_output_path, currfile_dir_out)
    return tex_output_path_pdf


def create_gridpaper_std(paperheight, paperwidth, patternsize, majorcolor, minorcolor):
    return create_gridpaper_std_file(
        paperheight,
        paperwidth,
        patternsize,
        majorcolor,
        minorcolor,
        "gridpapers_std_template.tex",
        "gp_std"
        )
