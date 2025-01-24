import zipfile
from pathlib import Path
from datetime import datetime
import pytz
import time
import random

from ..utilities.util_functions import merge_files, convert_to_pdf


# uses a macro to order pre defined angles

def random_angles():
    text = "{acuteangle, rightangle, obtuseangle, straightangle, reflexangle, revolution}"
    # Step 1: Convert the text string into a list of words
    words = text.strip("{}").split(", ")
    # Step 2: Shuffle the list of words
    random.shuffle(words)
    # Step 3: Join the shuffled list of words back into a text string
    shuffled_text = "{" + ", ".join(words) + "}"
    return shuffled_text


def worksheet_types_of_angles(title_text, tex_template_file, tex_ans_template_file, output_filename_prefix, file_type="pdf"):
    output_dir = Path(__file__).parent.parent.parent
    timestamp = "{date:%Y_%b_%d_%H_%M_%S}".format(date=datetime.now(tz=pytz.timezone("Australia/Melbourne")))
    currfile_dir_out = output_dir / "output"
    Path(currfile_dir_out).mkdir(parents=True, exist_ok=True)

    currfile_dir = Path(__file__).parent
    tex_template_path = currfile_dir / tex_template_file
    texans_template_path = currfile_dir / tex_ans_template_file

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

    # Generate the <<diagram>> replacement tex
    new_diagram_list = random_angles()
    # Replace the <<diagram>> placeholder in the LaTeX template
    tex_template_txt = tex_template_txt.replace("<<macro_order>>", new_diagram_list)
    tex_template_txt_ans = tex_template_txt_ans.replace("<<macro_order>>", new_diagram_list)
    tex_template_txt = tex_template_txt.replace("<<title>>", title_text)
    tex_template_txt_ans = tex_template_txt_ans.replace("<<title>>", title_text)
    # Write the question diagram tex to an output file
    with open(tex_output_path, "w") as outfile:
        outfile.write(tex_template_txt)
    # Write the answer diagram tex to an output file
    with open(tex_output_path_ans, "w") as outfile:
        outfile.write(tex_template_txt_ans)

    # Wait for the files to be created
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


def create_worksheet_types_of_angles(title_text="Types of Angles", file_type="pdf"):
    return worksheet_types_of_angles(
        title_text,
        "types_of_angles_q_template.tex",
        "types_of_angles_ans_template.tex",
        "ang_type",
        file_type,
    )

# create_worksheet_types_of_angles(title_text="Types of Angles")