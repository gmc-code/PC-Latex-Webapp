import zipfile
from pathlib import Path
from datetime import datetime
import pytz
import time

from ..utilities.util_functions import merge_files, convert_to_pdf
from .angles_in_parallel_lines_functions import choose_angles_in_parallel_lines_dict
# # for in file testing:
# from util_functions import merge_files, convert_to_pdf
# from angles_in_parallel_lines_functions import choose_angles_in_parallel_lines_dict



def make_diagram(tex_diagram_template_txt, tex_keys_q, process_dict):
    tex_diagram_template_txt_ans = tex_diagram_template_txt
    posttext = r"\vspace{1cm}"
    for key, value in process_dict.items():
        tex_diagram_template_txt_ans = tex_diagram_template_txt_ans.replace("<<" + key + ">>", value)
    for key, value in process_dict.items():
        if key in tex_keys_q:
            tex_diagram_template_txt = tex_diagram_template_txt.replace("<<" + key + ">>", value)
        else:
            tex_diagram_template_txt = tex_diagram_template_txt.replace("<<" + key + ">>", "\\dotuline{~~~~~~~}")
            # non breaking spaces for gaps
    return tex_diagram_template_txt + posttext, tex_diagram_template_txt_ans + posttext


def generate_diagram_text(numq, q_per_column, process_func, tex_diagram_template_txt):
    q_per_page = q_per_column * 2
    # generate diagrams text and text for answers
    diagrams_text = ""
    diagrams_text_ans = ""
    # add the headtext
    # must have no space in \end{minipage}\columnbreak for column break to occur at correct place.
    headtext_col = r"""\columnbreak
    """
    headtext_page = r"""\newpage
    """
    # headtext_page = r'''\newpage ~ \newline ~ \newline'''

    for i in range(1, numq + 1):
        img_tex, img_tex_ans = process_func(tex_diagram_template_txt)
        diagrams_text += img_tex
        diagrams_text_ans += img_tex_ans
        # Add page break only if it's a full page and there are more questions
        if i % q_per_page == 0 and numq + 1 > i:
            diagrams_text += headtext_page
            diagrams_text_ans += headtext_page
        # Add column break only if it's a full column and not the first question
        elif i % q_per_column == 0 and i > 1 and numq + 1 > i:
            diagrams_text += headtext_col
            diagrams_text_ans += headtext_col
    # Ensure no page break is added at the end if the last page is not full
    if numq % q_per_page != 0:
        diagrams_text = diagrams_text.rstrip(headtext_page)
        diagrams_text_ans = diagrams_text_ans.rstrip(headtext_page)
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

# % keys for questions, omit ans keys
# tex_keys_q = ['aval', 'bval', 'cval', 'dval', 'eval', 'fval', 'gval', 'hval', 'angle_to_find_value']

def create_booklet_parallel_lines(numq=8, num=5, title_text="Angles in Parallel Lines", file_type="pdf"):
    tex_keys_q = ["rotationAngle","parIstartx","parIstarty","parIendx","parIendy","parIIstartx","parIIstarty",
                "parIIendx","parIIendy","transstartx","transstarty","transendx","transendy","anglestext",
                "alabel","blabel","clabel","dlabel","elabel","flabel","glabel","hlabel","angle_to_find",]

    q_per_column = 4

    def make_diagram_wrapper(tex_diagram_template_txt):
        return make_diagram(tex_diagram_template_txt, tex_keys_q, choose_angles_in_parallel_lines_dict(num))

    return create_booklet(
        numq,
        title_text,
        q_per_column,
        make_diagram_wrapper,
        "angles_in_parallel_lines_booklet_template.tex",
        "angles_in_parallel_lines_booklet_ans_template.tex",
        "angles_in_parallel_lines_booklet_diagram_template.tex",
        "pla",
        file_type,
    )



# create_booklet_parallel_lines(numq=8, num=7, title_text="Angles in Parallel Lines", file_type="pdf")
