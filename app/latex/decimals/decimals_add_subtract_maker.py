import zipfile
from pathlib import Path
from datetime import datetime
import pytz
import time

from ..utilities.util_functions import merge_files, convert_to_pdf
from .decimals_functions import get_dec_dict
# for in file testing:
# from app.utilities.util_functions import merge_files, convert_to_pdf
# from decimals_functions import get_dec_dict


def make_diagram(tex_diagram_template_txt, tex_keys_q, process_dict):
    tex_diagram_template_txt_ans = tex_diagram_template_txt
    posttext = "" # r"\vspace{-2pt}"
    for key, value in process_dict.items():
        tex_diagram_template_txt_ans = tex_diagram_template_txt_ans.replace("<<" + key + ">>", value)
    for key, value in process_dict.items():
        if key not in tex_keys_q:
            tex_diagram_template_txt = tex_diagram_template_txt.replace("<<" + key + ">>", value)
        else:
            tex_diagram_template_txt = tex_diagram_template_txt.replace("<<" + key + ">>", "")
    return tex_diagram_template_txt + posttext, tex_diagram_template_txt_ans + posttext


def generate_diagram_text(numq, q_per_column, process_func, tex_diagram_template_txt):
    q_per_page = q_per_column * 3
    # generate diagrams text and text for answers
    diagrams_text = ""
    diagrams_text_ans = ""
    # add the headtext
    # must have no space in \end{minipage}\columnbreak for column break to occur at correct place.
    # \vspace*{0pt}: * forces it to apply at top of column or page
    headtext_col = r"""\columnbreak\vspace*{0pt}
    """
    headtext_page = r"""\newpage
    """
    # headtext_page = r'''\newpage ~ \newline ~ \newline'''

    for i in range(1, numq + 1):
        img_tex, img_tex_ans = process_func(tex_diagram_template_txt)
        diagrams_text += img_tex
        diagrams_text_ans += img_tex_ans
        if i % q_per_page == 0 and numq + 1 > i:
            diagrams_text += headtext_page
            diagrams_text_ans += headtext_page
        elif i % q_per_column == 0 and i > 1 and numq + 1 > i:
            diagrams_text += headtext_col
            diagrams_text_ans += headtext_col
    return diagrams_text, diagrams_text_ans


def create_booklet(numq, title_text, q_per_column, process_func, tex_template_file, tex_ans_template_file, tex_diagram_template_file, output_filename_prefix, file_type="pdf"):
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
    diagram_text, diagram_text_ans = generate_diagram_text(numq, q_per_column, process_func, tex_diagram_template_txt)

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

# (numq, operation, numip, numdp, title_text, file_type=file_type)
def create_booklet_add_sub(numq=27, num=1, numip=1, numdp=1, title_text="Decimals", file_type="pdf"):
    # tex_keys = ["num1", "num2", "process", "numip", "numdp"]
    tex_keys_q = ["answer"]
    q_per_column = 9

    def make_diagram_wrapper(tex_diagram_template_txt):
        return make_diagram(tex_diagram_template_txt, tex_keys_q, get_dec_dict(num, numip, numdp))

    return create_booklet(
        numq,
        title_text,
        q_per_column,
        make_diagram_wrapper,
        "decimals_booklet_template.tex",
        "decimals_booklet_ans_template.tex",
        "decimals_booklet_diagram_template.tex",
        "dec_as",
        file_type,
    )


# create_booklet_add_sub(numq=50, num=1, numip=1, numdp=1, title_text="Decimals", file_type="pdf")
