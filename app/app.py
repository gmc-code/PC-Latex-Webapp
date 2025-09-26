from pathlib import Path
import os
import glob

# from flask import Flask, render_template, request, send_file, after_this_request, jsonify, url_for, send_from_directory, render_template_string
from flask import Flask, render_template, request, send_file, after_this_request, abort, url_for

import latex.backtracking.backtracking_maker as backtrack

import latex.numberlines.number_lines_maker as numline
import latex.numberlines.number_lines_maker_blank as numlineblk

import latex.equations.equations_maker as equations
import latex.check_solutions.check_solution_maker as checksol

import latex.decimals.decimals_add_subtract_maker as decas
import latex.types_of_angles.types_of_angles_maker as angtyp

import latex.angles_in_parallel_lines.angles_in_parallel_lines_maker as pla
import latex.external_angle_to_a_triangle.ext_angle_to_triangle_maker as extang
import latex.angles_in_a_right_angled_triangle.angles_in_a_rt_triangle_maker as rttriang
import latex.angles_in_an_isosceles_triangle.angles_in_iso_triangle_maker as isotriang
import latex.angles_in_a_triangle.angles_in_a_triangle_maker as angtri
import latex.measuring_angles.measuring_angles_maker as measang

import latex.coordinates.coordinates_maker as coords

import latex.area_of_a_square.area_of_a_square_maker as areasq
import latex.area_of_a_rectangle.area_of_a_rectangle_maker as arearect

import latex.paper.lined_paper_maker as linedpaper
import latex.gridpapers.grids_isometric_maker as grdpiso
import latex.gridpapers.gridpapers_std_maker as grdpstd
import latex.gridpapers.gridpapers_dot_maker as grdpdot
import latex.gridpapers.gridpapers_tri_maker as grdptri


app = Flask(__name__)

##########################################################################

# backtrack_onestep_create has an example of using 400 and 500 aborts

##########################################################################

# backtracking, equations, check solutions
ops = {"Random": 5, "Addition": 1, "Subtraction": 2, "Multiplication": 3, "Division": 4}
# number lines
nlops = {"Random": 6, "Plus": 1, "Minus Negative": 2, "Minus": 3, "Minus Positive": 4, "Plus Negative": 5}
# integer places
ipops = {"1": 1, "2": 2, "3": 3, "4": 4}
# decimal places
dpops = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
# decimals_add_sub,
decops = {"Random": 3, "Addition": 1, "Subtraction": 2}
# parallel lines angles
plops = {"Random": 7, "Corresponding": 1, "Alternate": 2, "Cointerior": 3, "Vertically Opposite": 4, "Consecutive Exterior": 5, "Alternate Exterior": 6}
# external angle to a triangle
eatops = {"Random": 4, "unknown A": 1, "unknown C": 2, "unknown external B": 3}
# isosceles triangle
isotops = {"Random": 3, "unknown unique angle": 1, "unknown paired angle": 2}
# measuring angles
maops = {"Random": 4, "Acute": 1, "Obtuse": 2, "Reflex": 3}
# gridpapers
patternsizes_ops = {"1cm": 3, "0.25cm": 1, "0.5cm": 2, "2cm": 4}
dotsizes_ops = {"0.7pt": 1, "1.0pt": 2, "1.4pt": 3, "2.0pt": 4}
# colours_ops = {"black": 1, "black!90!white": 2, "gray": 3, "black!60!white": 4, "black!40!white": 5, "black!40!white": 6}
colours_ops = {
    "Black": "black",  # 100% black
    "Charcoal": "black!90!white",  # 90% black
    "Dark Gray": "black!80!white",  # 80% black
    "Slate Gray": "black!70!white",  # 70% black
    "Gray": "black!60!white",  # 60% black
    "Medium Gray": "black!50!white",  # 50% black
    "Light Gray": "black!40!white",  # 40% black
    "Soft Gray": "black!30!white",  # 30% black
    "Pale Gray": "black!20!white",  # 20% black
    "Mist Gray": "black!10!white",  # 10% black
    "White": "white",  # 0% black
}

# grids_isometric
gridorientation_ops = ["vertical", "horizontal"]
isometric_dotfilltype_ops = ["filled", "open"]
isometric_dotspacing_ops = ["0.8", "0.5", "1.0", "1.5", "2.0"]
isometric_dotsize_ops = ["0.8pt", "1.2pt", "1.6pt", "2.0pt", "3.0pt"]
isometric_dotlinewidth_ops = ["0.4pt", "0.6pt", "0.8pt", "1.0pt", "2.0pt"]


##########################################################################


@app.route("/")
def index():
    """Renders the home page."""
    return render_template(
        "index.html",
        title="Home Page",
    )


# @app.route("/samples")
# def samples():
#     """Renders the samples page."""
#     return render_template(
#         "samples.html",
#         title="Sample pdfs",
#     )

@app.errorhandler(400)
def bad_request(error):
    return render_template("400.html", error=error), 400

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html", error=error), 500

@app.errorhandler(504)
def gateway_timeout(e):
    return render_template("504.html", error=e), 504



##########################################################################

def parse_and_clamp(form, field_name, default, min_val, max_val, cast_type=float):
    """
    Safely parse a numeric field from a form and clamp it to a specified range.

    Parameters:
        form (ImmutableMultiDict): The request.form object.
        field_name (str): The name of the field to retrieve.
        default (float or int): The fallback value if parsing fails.
        min_val (float or int): Minimum allowed value.
        max_val (float or int): Maximum allowed value.
        cast_type (type): Type to cast the value to (float or int).

    Returns:
        float or int: The clamped numeric value.
    """
    try:
        value = cast_type(form.get(field_name, default))
    except (ValueError, TypeError):
        value = default
    return max(min_val, min(value, max_val))



##########################################################################

@app.route("/backtrack_onestep")
def backtrack_onestep():
    return render_template(
        "genform_tqof.html",
        title="One-Step Backtracking",
        operation_label="Operation",
        ops=list(ops.keys()),  # Ensure compatibility with template rendering
        link="/backtrack_onestep_create",
        num_per_page=10,       # Pass as integer, not string
        min_questions=1,
        max_questions=100,
        img_filename="backtrack_onestep.png",
        pdf_filename="backtrack_onestep.pdf",
        title_text="1-step Backtracking",
    )

@app.route("/backtrack_onestep_create", methods=["POST"])
def backtrack_onestep_create():
    # Safely parse and clamp numq
    numq = parse_and_clamp(request.form, "numq", 10, 1, 100, cast_type=int)
    # try:
    #     numq = int(request.form.get("numq", 10))
    # except (ValueError, TypeError):
    #     numq = 10
    # numq = max(1, min(numq, 100))

    # Validate operation key
    operation_key = request.form.get("operation")
    # not in
    if operation_key not in ops:
        abort(400, description="Invalid operation selected.")
    operation = ops[operation_key]

    # Get title text with fallback
    title_text = request.form.get("title_text") or "1-step Backtracking"

    # Determine file type and MIME type
    file_type = request.form.get("file_type", "pdf").lower()
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")

    # Generate file with error handling
    try:
        file = backtrack.create_booklet_1step(numq, operation, title_text, file_type=file_type)
    except Exception as e:
        abort(500, description=f"Error generating booklet: {str(e)}")

    return send_file(file, as_attachment=True, mimetype=mimetype)




# @app.route("/backtrack_onestep")
# def backtrack_onestep():
#     return render_template(
#         "genform_tqof.html",
#         title="One-Step Backtracking",
#         operation_label="Operation",
#         ops=ops.keys(),
#         link="/backtrack_onestep_create",
#         num_per_page="10",
#         min_questions="1",
#         max_questions="100",
#         img_filename="backtrack_onestep.png",
#         pdf_filename="backtrack_onestep.pdf",
#         title_text="1-step Backtracking",
#     )


# @app.route("/backtrack_onestep_create", methods=["POST"])
# def backtrack_onestep_create():
#     # Safely parse numq
#     try:
#         numq = int(request.form.get("numq", 10))
#     except ValueError:
#         numq = 10  # fallback default
#     # Clamp to range to prevent issue with user manual entry although js should catch it
#     min_q = 1
#     max_q = 100
#     numq = max(min_q, min(numq, max_q))
#     #
#     operation = ops[request.form.get("operation")]
#     title_text = request.form.get("title_text")
#     file_type = request.form.get("file_type", "pdf")
#     mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
#     file = backtrack.create_booklet_1step(numq, operation, title_text, file_type=file_type)
#     return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/backtrack_twostep")
def backtrack_twostep():
    return render_template(
        "genform_tq2of.html",
        title="Two-Step Backtracking",
        ops=ops.keys(),
        link="/backtrack_twostep_create",
        num_per_page="10",
        min_questions="1",
        max_questions="100",
        img_filename="backtrack_twostep.png",
        pdf_filename="backtrack_twostep.pdf",
        title_text="2-step Backtracking",
    )


@app.route("/backtrack_twostep_create", methods=["POST"])
def backtrack_twostep_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 10))
    except ValueError:
        numq = 10  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 100
    numq = max(min_q, min(numq, max_q))
    #
    operation = ops[request.form.get("operation")]
    operation2 = ops[request.form.get("operation2")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = backtrack.create_booklet_2step(numq, operation, operation2, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/backtrack_twostep_buildexpression")
def backtrack_twostep_buildexpression():
    return render_template(
        "genform_tq2of.html",
        title="Two-Step Backtracking Build Expression",
        ops=ops.keys(),
        link="/backtrack_twostep_buildexpression_create",
        num_per_page="20",
        min_questions="1",
        max_questions="100",
        img_filename="backtrack_twostep_buildexpression.png",
        pdf_filename="backtrack_twostep_buildexpression.pdf",
        title_text="Build expression",
    )


@app.route("/backtrack_twostep_buildexpression_create", methods=["POST"])
def backtrack_twostep_buildexpression_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 20))
    except ValueError:
        numq = 20  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 100
    numq = max(min_q, min(numq, max_q))
    #
    operation = ops[request.form.get("operation")]
    operation2 = ops[request.form.get("operation2")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = backtrack.create_booklet_2step_buildexp(numq, operation, operation2, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/backtrack_twostep_buildexpression_inverse")
def backtrack_twostep_buildexpression_inverse():
    return render_template(
        "genform_tq2of.html",
        title="Two-Step Backtracking Build Expression Inverse",
        ops=ops.keys(),
        link="/backtrack_twostep_buildexpression_inverse_create",
        num_per_page="14",
        min_questions="1",
        max_questions="140",
        img_filename="backtrack_twostep_buildexpression_inverse.png",
        pdf_filename="backtrack_twostep_buildexpression_inverse.pdf",
        title_text="Build expression inverse",
    )


@app.route("/backtrack_twostep_buildexpression_inverse_create", methods=["POST"])
def backtrack_twostep_buildexpression_inverse_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 14))
    except ValueError:
        numq = 14  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 140
    numq = max(min_q, min(numq, max_q))
    #
    operation = ops[request.form.get("operation")]
    operation2 = ops[request.form.get("operation2")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = backtrack.create_booklet_2step_buildexpinv(numq, operation, operation2, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/backtrack_twostep_fromexpression")
def backtrack_twostep_fromexpression():
    return render_template(
        "genform_tq2of.html",
        title="Two-Step Backtracking Build From Expression",
        ops=ops.keys(),
        link="/backtrack_twostep_fromexpression_create",
        num_per_page="14",
        min_questions="1",
        max_questions="140",
        img_filename="backtrack_twostep_fromexpression.png",
        pdf_filename="backtrack_twostep_fromexpression.pdf",
        title_text="Build from expression",
    )


@app.route("/backtrack_twostep_fromexpression_create", methods=["POST"])
def backtrack_twostep_fromexpression_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 14))
    except ValueError:
        numq = 14  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 140
    numq = max(min_q, min(numq, max_q))
    #
    operation = ops[request.form.get("operation")]
    operation2 = ops[request.form.get("operation2")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = backtrack.create_booklet_2step_fromexp(numq, operation, operation2, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/backtrack_twostep_fromequation")
def backtrack_twostep_fromequation():
    return render_template(
        "genform_tq2of.html",
        title="Two-Step Backtracking From Equation",
        ops=ops.keys(),
        link="/backtrack_twostep_fromequation_create",
        num_per_page="10",
        min_questions="1",
        max_questions="100",
        img_filename="backtrack_twostep_fromequation.png",
        pdf_filename="backtrack_twostep_fromequation.pdf",
        title_text="Build from equation",
    )


@app.route("/backtrack_twostep_fromequation_create", methods=["POST"])
def backtrack_twostep_fromequation_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 10))
    except ValueError:
        numq = 10  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 100
    numq = max(min_q, min(numq, max_q))
    #
    operation = ops[request.form.get("operation")]
    operation2 = ops[request.form.get("operation2")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = backtrack.create_booklet_2step_fromeq(numq, operation, operation2, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/backtrack_twostep_blank")
def backtrack_twostep_blank():
    return render_template(
        "genform_tq.html",
        title="Two-Step Backtracking Blank",
        link="/backtrack_twostep_blank_create",
        num_per_page="10",
        min_questions="1",
        max_questions="100",
        img_filename="backtrack_twostep_blank.png",
        pdf_filename="backtrack_twostep_blank.pdf",
        title_text="2-step Backtracking",
    )


@app.route("/backtrack_twostep_blank_create", methods=["POST"])
def backtrack_twostep_blank_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 10))
    except ValueError:
        numq = 10  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 100
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    file = backtrack.create_booklet_2step_blank(numq, title_text)
    return send_file(file, as_attachment=True, mimetype="application/pdf")



##########################################################################
# number lines
##########################################################################


@app.route("/number_lines")
def number_lines():
    # "Enter 1,2,3,4,5 or 6 for plus,minus_neg,minus,minus_pos,plus_neg,random \n"
    return render_template(
        "genform_tqof.html",
        title="Number Lines",
        operation_label="Operation",
        ops=nlops.keys(),
        link="/number_lines_create",
        num_per_page="8",
        min_questions="1",
        max_questions="80",
        img_filename="number_lines.png",
        pdf_filename="number_lines.pdf",
        title_text="Number Lines",
    )


@app.route("/number_lines_create", methods=["POST"])
def number_lines_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 8))
    except ValueError:
        numq = 8  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 80
    numq = max(min_q, min(numq, max_q))
    #
    operation = nlops[request.form.get("operation")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = numline.create_booklet_numberline(numq, operation, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/number_lines_0to20")
def number_lines_0to20():
    # "Enter 1,2,3,4,5 or 6 for plus,minus_neg,minus,minus_pos,plus_neg,random \n"
    return render_template(
        "genform_tqof.html",
        title="Number Lines 0 to 20",
        operation_label="Operation",
        ops=nlops.keys(),
        link="/number_lines_0to20_create",
        num_per_page="8",
        min_questions="1",
        max_questions="80",
        img_filename="number_lines_0to20.png",
        pdf_filename="number_lines_0to20.pdf",
        title_text="Number Lines +",
    )


@app.route("/number_lines_0to20_create", methods=["POST"])
def number_lines_0to20_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 8))
    except ValueError:
        numq = 8  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 80
    numq = max(min_q, min(numq, max_q))
    #
    operation = nlops[request.form.get("operation")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = numline.create_booklet_numberline_0to20(numq, operation, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/number_lines_neg20to0")
def number_lines_neg20to0():
    # "Enter 1,2,3,4,5 or 6 for plus,minus_neg,minus,minus_pos,plus_neg,random \n"
    return render_template(
        "genform_tqof.html",
        title="Number Lines -20 to 0",
        operation_label="Operation",
        ops=nlops.keys(),
        link="/number_lines_neg20to0_create",
        num_per_page="8",
        min_questions="1",
        max_questions="80",
        img_filename="number_lines_neg20to0.png",
        pdf_filename="number_lines_neg20to0.pdf",
        title_text="Number Lines -",
    )


@app.route("/number_lines_neg20to0_create", methods=["POST"])
def number_lines_neg20to0_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 8))
    except ValueError:
        numq = 8  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 80
    numq = max(min_q, min(numq, max_q))
    #
    operation = nlops[request.form.get("operation")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = numline.create_booklet_numberline_neg20to0(numq, operation, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/number_lines_blank")
def number_lines_blank():
    return render_template(
        "genform_tq.html",
        title="Number Lines Blank",
        link="/number_lines_blank_create",
        num_per_page="8",
        min_questions="1",
        max_questions="80",
        img_filename="number_lines_blank.png",
        pdf_filename="number_lines_blank.pdf",
        title_text="Number Lines",
    )


@app.route("/number_lines_blank_create", methods=["POST"])
def number_lines_blank_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 8))
    except ValueError:
        numq = 8  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 80
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    file = numlineblk.create_booklet_numberline_blank(numq, title_text)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################


@app.route("/number_lines_blank_0to20")
def number_lines_blank_0to20():
    return render_template(
        "genform_tq.html",
        title="Number Lines Blank 0 to 20",
        link="/number_lines_blank_0to20_create",
        num_per_page="8",
        min_questions="1",
        max_questions="80",
        img_filename="number_lines_blank_0to20.png",
        pdf_filename="number_lines_blank_0to20.pdf",
        title_text="Number Lines +",
    )


@app.route("/number_lines_blank_0to20_create", methods=["POST"])
def number_lines_blank_0to20_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 8))
    except ValueError:
        numq = 8  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 80
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    file = numlineblk.create_booklet_numberline_blank_0to20(numq, title_text)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################


@app.route("/number_lines_blank_neg20to0")
def number_lines_blank_neg20to0():
    return render_template(
        "genform_tq.html",
        title="Number Lines Blank -20 to 0",
        link="/number_lines_blank_neg20to0_create",
        num_per_page="8",
        min_questions="1",
        max_questions="80",
        img_filename="number_lines_blank_neg20to0.png",
        pdf_filename="number_lines_blank_neg20to0.pdf",
        title_text="Number Lines -",
    )


@app.route("/number_lines_blank_neg20to0_create", methods=["POST"])
def number_lines_blank_neg20to0_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 8))
    except ValueError:
        numq = 8  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 80
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    file = numlineblk.create_booklet_numberline_blank_neg20to0(numq, title_text)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################
# equations
##########################################################################


@app.route("/equations_onestep_inverse_operations")
def equations_onestep_inverse_operations():
    return render_template(
        "genform_tqof.html",
        title="One-Step Equations",
        operation_label="Operation",
        ops=ops.keys(),
        link="/equations_onestep_inverse_operations_create",
        num_per_page="16",
        min_questions="1",
        max_questions="160",
        img_filename="equations_onestep_inverse_operations.png",
        pdf_filename="equations_onestep_inverse_operations.pdf",
        title_text="1-step Equations",
    )


@app.route("/equations_onestep_inverse_operations_create", methods=["POST"])
def equations_onestep_inverse_operations_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 16))
    except ValueError:
        numq = 16  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 160
    numq = max(min_q, min(numq, max_q))
    #
    operation = ops[request.form.get("operation")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = equations.create_booklet_1step(numq, operation, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################


@app.route("/equations_twostep_inverse_operations")
def equations_twostep_inverse_operations():
    return render_template(
        "genform_tq2of.html",
        title="Two-Step Equations",
        ops=ops.keys(),
        link="/equations_twostep_inverse_operations_create",
        num_per_page="10",
        min_questions="1",
        max_questions="100",
        img_filename="equations_twostep_inverse_operations.png",
        pdf_filename="equations_twostep_inverse_operations.pdf",
        title_text="2-step Equations",
    )


@app.route("/equations_twostep_inverse_operations_create", methods=["POST"])
def equations_twostep_inverse_operations_create():
    # Safely parse numq
    numq = parse_and_clamp(request.form, "numq", 10, 1, 100, cast_type=int)

    # try:
    #     numq = int(request.form.get("numq", 10))
    # except ValueError:
    #     numq = 10  # fallback default
    # # Clamp to range to prevent issue with user manual entry although js should catch it
    # min_q = 1
    # max_q = 100
    # numq = max(min_q, min(numq, max_q))
    #
    operation = ops[request.form.get("operation")]
    operation2 = ops[request.form.get("operation2")]
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = equations.create_booklet_2step(numq, operation, operation2, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# check solutions
##########################################################################


@app.route("/check_solution_onestep")
def check_solution_onestep():
    return render_template(
        "genform_tqof.html",
        title="Check Solution One-Step",
        operation_label="Operation",
        ops=ops.keys(),
        link="/check_solution_onestep_create",
        num_per_page="10",
        min_questions="1",
        max_questions="100",
        img_filename="check_solution_onestep.png",
        pdf_filename="check_solution_onestep.pdf",
        title_text="1-step Check Solution",
    )


@app.route("/check_solution_onestep_create", methods=["POST"])
def check_solution_onestep_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 10))
    except ValueError:
        numq = 10  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 100
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    operation = ops[request.form.get("operation")]
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = checksol.create_booklet_1step(numq, operation, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


####################################################################################################


@app.route("/check_solution_twostep")
def check_solution_twostep():
    return render_template(
        "genform_tq2of.html",
        title="Check Solution Two-Step",
        ops=ops.keys(),
        link="/check_solution_twostep_create",
        num_per_page="10",
        min_questions="1",
        max_questions="100",
        img_filename="check_solution_twostep.png",
        pdf_filename="check_solution_twostep.pdf",
        title_text="2-step Check Solution",
    )


@app.route("/check_solution_twostep_create", methods=["POST"])
def check_solution_twostep_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 10))
    except ValueError:
        numq = 10  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 100
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    operation = ops[request.form.get("operation")]
    operation2 = ops[request.form.get("operation2")]
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = checksol.create_booklet_2step(numq, operation, operation2, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# decimals
##########################################################################


@app.route("/decimals_add_subtract")
def decimals_add_subtract():
    return render_template(
        "decimals_form.html",
        title="Decimals Short Addition Subtraction",
        ops=decops.keys(),
        ipops=ipops.keys(),
        dpops=dpops.keys(),
        link="/decimals_add_subtract_create",
        num_per_page="27",
        min_questions="1",
        max_questions="108",
        img_filename="decimals_add.png",
        pdf_filename="decimals_add_subtract.pdf",
        title_text="Decimals Short Addition Subtraction",
    )


@app.route("/decimals_add_subtract_create", methods=["POST"])
def decimals_add_subtract_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 27))
    except ValueError:
        numq = 27  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 108
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    operation = decops[request.form.get("operation")]
    numip = int(ipops[request.form.get("numip")])
    numdp = int(dpops[request.form.get("numdp")])
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = decas.create_booklet_add_sub(numq, operation, numip, numdp, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# angle types --single page with random order
##########################################################################
# continue from here


@app.route("/types_of_angles")
def types_of_angles():
    return render_template(
        "genform_tf.html",
        title="Types of Angles",
        link="/types_of_angles_create",
        img_filename="types_of_angles.png",
        pdf_filename="types_of_angles.pdf",
        title_text="Types of Angles",
    )


@app.route("/types_of_angles_create", methods=["POST"])
def types_of_angles_create():
    title_text = request.form.get("title_text")
    file = angtyp.create_worksheet_types_of_angles(title_text)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################
# parallel lines angles
##########################################################################


@app.route("/angles_in_parallel_lines")
def angles_in_parallel_lines():
    return render_template(
        "genform_tqof.html",
        title="Angles in Parallel Lines",
        operation_label="Type of Angles",
        ops=plops.keys(),
        link="/angles_in_parallel_lines_create",
        num_per_page="8",
        min_questions="1",
        max_questions="80",
        img_filename="corresponding_angles.png",
        pdf_filename="parallel_lines_angles.pdf",
        title_text="Angles in Parallel Lines",
    )


@app.route("/angles_in_parallel_lines_create", methods=["POST"])
def angles_in_parallel_lines_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 8))
    except ValueError:
        numq = 8  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 80
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    angle_type = plops[request.form.get("operation")]
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = pla.create_booklet_parallel_lines(numq, angle_type, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# external angle to a triangle
##########################################################################


@app.route("/external_angle_to_a_triangle")
def external_angle_to_a_triangle():
    return render_template(
        "genform_tqof.html",
        title="External Angle to a Triangle",
        operation_label="Angle",
        ops=eatops.keys(),
        link="/external_angle_to_a_triangle_create",
        num_per_page="4",
        min_questions="1",
        max_questions="40",
        img_filename="ext_angle_to_triangle.png",
        pdf_filename="ext_angle_to_triangle.pdf",
        title_text="External Angle to a Triangle",
    )


@app.route("/external_angle_to_a_triangle_create", methods=["POST"])
def external_angle_to_a_triangle_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 4))
    except ValueError:
        numq = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 40
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    unknown_position = eatops[request.form.get("operation")]
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = extang.create_booklet_ext_angle_to_triangle(numq, title_text, unknown_position, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# angles in a right angled triangle
##########################################################################


@app.route("/angles_in_a_right_angled_triangle")
def angles_in_a_right_angled_triangle():
    return render_template(
        "genform_tqf.html",
        title="Angles in a Right Angled Triangle",
        link="/angles_in_a_right_angled_triangle_create",
        num_per_page="4",
        min_questions="1",
        max_questions="40",
        img_filename="angles_in_a_rt_triangle.png",
        pdf_filename="angles_in_a_rt_triangle.pdf",
        title_text="Angles in a Right Angled Triangle",
    )


@app.route("/angles_in_a_right_angled_triangle_create", methods=["POST"])
def angles_in_a_right_angled_triangle_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 4))
    except ValueError:
        numq = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 40
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = rttriang.create_booklet_angles_in_a_rt_triangle(numq, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# angles in an iscoceles triangle
##########################################################################


@app.route("/angles_in_an_isosceles_triangle")
def angles_in_an_isosceles_triangle():
    return render_template(
        "genform_tqof.html",
        title="Angles in an Isosceles Triangle",
        operation_label="Angle",
        ops=isotops.keys(),
        link="/angles_in_an_isosceles_triangle_create",
        num_per_page="4",
        min_questions="1",
        max_questions="40",
        img_filename="angles_in_iso_triangle.png",
        pdf_filename="angles_in_iso_triangle.pdf",
        title_text="Angles in an Isosceles Triangle",
    )


@app.route("/angles_in_an_isosceles_triangle_create", methods=["POST"])
def angles_in_an_isosceles_triangle_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 4))
    except ValueError:
        numq = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 40
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    unknown_position = isotops[request.form.get("operation")]
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = isotriang.create_booklet_iso_angle_in_triangle(numq, title_text, unknown_position, file_type=file_type)  #
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# angles in a triangle
##########################################################################


@app.route("/angles_in_a_triangle")
def angles_in_a_triangle():
    return render_template(
        "genform_tqf.html",
        title="Angles in a Triangle",
        link="/angles_in_a_triangle_create",
        num_per_page="4",
        min_questions="1",
        max_questions="40",
        img_filename="angles_in_a_triangle.png",
        pdf_filename="angles_in_a_triangle.pdf",
        title_text="Angles in a Triangle",
    )


@app.route("/angles_in_a_triangle_create", methods=["POST"])
def angles_in_a_triangle_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 4))
    except ValueError:
        numq = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 40
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = angtri.create_booklet_angle_in_a_triangle(numq, title_text, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# measuring angles
##########################################################################


@app.route("/measuring_angles")
def measuring_angles():
    return render_template(
        "genform_tqof.html",
        title="Measuring Angles",
        operation_label="Type of Angles",
        ops=maops.keys(),
        link="/measuring_angles_create",
        num_per_page="6",
        min_questions="1",
        max_questions="60",
        img_filename="measuring_angles.png",
        pdf_filename="measuring_angles.pdf",
        title_text="Measuring Angles",
    )


@app.route("/measuring_angles_create", methods=["POST"])
def measuring_angles_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 6))
    except ValueError:
        numq = 6  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 60
    numq = max(min_q, min(numq, max_q))
    #
    title_text = request.form.get("title_text")
    angle_type = int(maops[request.form.get("operation")])
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = measang.create_booklet_angles_for_measuring(numq, title_text, angle_type, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# paper
##########################################################################


@app.route("/lined_paper")
def lined_paper():
    return render_template(
        "lined_paper_form.html",
        title="Lined Paper",
        link="/lined_paper_create",
        num_lines="4",
        min_lines="1",
        max_lines="26",
        img_filename="lined_paper.png",
        pdf_filename="lined_paper.pdf",
    )


@app.route("/lined_paper_create", methods=["POST"])
def lined_paper_create():
    # Safely parse num_lines
    try:
        num_lines = int(request.form.get("num_lines", 4))
    except ValueError:
        num_lines = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 26
    num_lines = max(min_q, min(num_lines, max_q))
    #
    # # Checkbox returns "on" if checked
    whole_page = request.form.get("whole_page") == "on"
    if whole_page:
        num_lines = 26
    file = linedpaper.create_lined_paper(num_lines)
    # Return the PDF as a response
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################
# grids_isometric
##########################################################################


@app.route("/grids_isometric")
def grids_isometric():
    return render_template(
        "grids_isometric_form.html",
        title="Grids Isometric",
        paperheight=29.7,
        paperwidth=21,
        vmargin=1.5,
        hmargin=1.5,
        op_gridorientations=gridorientation_ops,
        op_dotfilltypes=isometric_dotfilltype_ops,
        op_dotspacings=isometric_dotspacing_ops,
        op_dotsizes=isometric_dotsize_ops,
        op_dotlinewidths=isometric_dotlinewidth_ops,
        op_colours=colours_ops.keys(),
        link="/grids_isometric_create",
        img_filename="grids_isometric.png",
        pdf_filename="grids_isometric.pdf",
    )




@app.route("/grids_isometric_create", methods=["POST"])
def grids_isometric_create():

    paperheight = parse_and_clamp(request.form, "paperheight", 29.7, 2.0, 29.7, cast_type=float)
    paperwidth  = parse_and_clamp(request.form, "paperwidth", 21.0, 5.0, 21.0, cast_type=float)
    vmargin     = parse_and_clamp(request.form, "vmargin", 2.5, 0.0, 2.5, cast_type=float)
    hmargin     = parse_and_clamp(request.form, "hmargin", 2.5, 0.0, 2.5, cast_type=float)


    # # Safely parse paperheight
    # try:
    #     paperheight = float(request.form.get("paperheight", 29.7))
    # except ValueError:
    #     paperheight = 29.7  # fallback default
    # # Clamp to range to prevent issue with user manual entry
    # min_height = 2.0
    # max_height = 29.7
    # paperheight = max(min_height, min(paperheight, max_height))

    # # Safely parse paperwidth
    # try:
    #     paperwidth = float(request.form.get("paperwidth", 21.0))
    # except ValueError:
    #     paperwidth = 21.0  # fallback default
    # min_width = 5.0
    # max_width = 21.0
    # paperwidth = max(min_width, min(paperwidth, max_width))

    # # Safely parse vmargin
    # try:
    #     vmargin = float(request.form.get("vmargin", 2.5))
    # except ValueError:
    #     vmargin = 2.5  # fallback default
    # min_vmargin = 0.0
    # max_vmargin = 2.5
    # vmargin = max(min_vmargin, min(vmargin, max_vmargin))

    # # Safely parse hmargin
    # try:
    #     hmargin = float(request.form.get("hmargin", 2.5))
    # except ValueError:
    #     hmargin = 2.5  # fallback default
    # min_hmargin = 0.0
    # max_hmargin = 2.5
    # hmargin = max(min_hmargin, min(hmargin, max_hmargin))


    gridorientation = request.form.get("op_gridorientation")
    dotfilltype = request.form.get("op_dotfilltype")
    dotspacing = request.form.get("op_dotspacing")
    dotsize = request.form.get("op_dotsize")
    dotlinewidth = request.form.get("op_dotlinewidth")
    dotcolor = colours_ops[request.form.get("op_colour")]

    file = grdpiso.create_grids_isometric(paperheight, paperwidth, vmargin, hmargin, gridorientation, dotfilltype, dotspacing, dotsize, dotlinewidth, dotcolor)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################
# gridpapers
##########################################################################


@app.route("/gridpapers")
def gridpapers():
    return render_template(
        "gridpapers_std_form_5o.html",
        title="GridPapers Standard",
        paperheight=29.7,
        paperwidth=21,
        op_patternsizes=patternsizes_ops.keys(),
        # op_major_colours=colours_ops.keys(),
        op_colours=colours_ops.keys(),
        link="/gridpapers_create",
        img_filename="gridpapers_standard.png",
        pdf_filename="gridpapers_standard.pdf",
    )


@app.route("/gridpapers_create", methods=["POST"])
def gridpapers_create():
    # use drop down selction, no need for item value even though defined
    paperheight = request.form.get("paperheight")
    paperwidth = request.form.get("paperwidth")
    patternsize = request.form.get("op_patternsize")
    majorcolor = colours_ops[request.form.get("op_major_colour")]
    minorcolor = colours_ops[request.form.get("op_minor_colour")]
    file = grdpstd.create_gridpaper_std(paperheight, paperwidth, patternsize, majorcolor, minorcolor)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################
# gridpapers_dots
##########################################################################


@app.route("/gridpapers_dot")
def gridpapers_dot():
    return render_template(
        "gridpapers_dot_form_5o.html",
        title="GridPapers Dots",
        paperheight=29.7,
        paperwidth=21,
        op_patternsizes=patternsizes_ops.keys(),
        op_dotsizes=dotsizes_ops.keys(),
        op_colours=colours_ops.keys(),
        link="/gridpapers_dot_create",
        img_filename="gridpapers_dots.png",
        pdf_filename="gridpapers_dots.pdf",
    )


@app.route("/gridpapers_dot_create", methods=["POST"])
def gridpapers_dot_create():
    # use drop down selction, no need for item value even though defined
    paperheight = request.form.get("paperheight")
    paperwidth = request.form.get("paperwidth")
    patternsize = request.form.get("op_patternsize")
    dotsize = request.form.get("op_dotsize")
    minorcolor = colours_ops[request.form.get("op_colour")]
    file = grdpdot.create_gridpaper_dot(paperheight, paperwidth, patternsize, dotsize, minorcolor)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################
# gridpapers_tri
##########################################################################


@app.route("/gridpapers_tri")
def gridpapers_tri():
    return render_template(
        "gridpapers_tri_form_4o.html",
        title="GridPapers Triangles",
        paperheight=29.7,
        paperwidth=21,
        op_patternsizes=patternsizes_ops.keys(),
        op_colours=colours_ops.keys(),
        link="/gridpapers_tri_create",
        img_filename="gridpapers_triangles.png",
        pdf_filename="gridpapers_triangles.pdf",
    )


@app.route("/gridpapers_tri_create", methods=["POST"])
def gridpapers_tri_create():
    # use drop down selction, no need for item value even though defined
    paperheight = request.form.get("paperheight")
    paperwidth = request.form.get("paperwidth")
    patternsize = request.form.get("op_patternsize")
    minorcolor = colours_ops[request.form.get("op_colour")]
    file = grdptri.create_gridpaper_tri(paperheight, paperwidth, patternsize, minorcolor)
    return send_file(file, as_attachment=True, mimetype="application/pdf")


##########################################################################
# coordinates
##########################################################################


@app.route("/coordinates")
def coordinates():
    return render_template(
        "coordinates_form.html",
        title="Coordinates",
        link="/coordinates_create",
        numq="1",
        min_questions="1",
        max_questions="10",
        num_points_per_question="10",
        min_points_per_question="4",
        max_points_per_question="20",
        img_filename="coordinates.png",
        pdf_filename="coordinates.pdf",
        title_text="Coordinates",
    )


@app.route("/coordinates_create", methods=["POST"])
def coordinates_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 4))
    except ValueError:
        numq = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 20
    numq = max(min_q, min(numq, max_q))
    #
    # Safely parse num_points
    try:
        num_points = int(request.form.get("num_points", 10))
    except ValueError:
        num_points = 10  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_num_points = 4
    max_num_points = 20
    num_points = max(min_num_points, min(num_points, max_num_points))
    #
    title_text = request.form.get("title_text")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = coords.create_booklet_coords(numq, title_text, num_points, file_type=file_type)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# area of a square
##########################################################################


@app.route("/area_of_a_square")
def area_of_a_square():
    return render_template(
        "genform_tqcbf.html",
        title="Area of a Square",
        link="/area_of_a_square_create",
        num_per_page="4",
        min_questions="1",
        max_questions="40",
        img_filename="area_of_a_square.png",
        pdf_filename="area_of_a_square.pdf",
        title_text="Area of a Square",
        checkbox_text="Show Dimension Lines",
    )


@app.route("/area_of_a_square_create", methods=["POST"])
def area_of_a_square_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 4))
    except ValueError:
        numq = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry
    min_q = 1
    max_q = 20
    numq = max(min_q, min(numq, max_q))
    #
    show_dimension_lines_bool = request.form.get("checkbox1") == "on"
    title_text = request.form.get("title_text", "")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = areasq.create_booklet_area_of_a_square(numq, title_text, file_type=file_type, show_dimension_lines_bool=show_dimension_lines_bool)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# area of a rectangle
##########################################################################


@app.route("/area_of_a_rectangle")
def area_of_a_rectangle():
    return render_template(
        "genform_tqcbf.html",
        title="Area of a Rectangle",
        link="/area_of_a_rectangle_create",
        num_per_page="4",
        min_questions="1",
        max_questions="40",
        img_filename="area_of_a_rectangle.png",
        pdf_filename="area_of_a_rectangle.pdf",
        title_text="Area of a Rectangle",
        checkbox_text="Show Dimension Lines",
    )


@app.route("/area_of_a_rectangle_create", methods=["POST"])
def area_of_a_rectangle_create():
    # Safely parse numq
    try:
        numq = int(request.form.get("numq", 4))
    except ValueError:
        numq = 4  # fallback default
    # Clamp to range to prevent issue with user manual entry although js should catch it
    min_q = 1
    max_q = 40
    numq = max(min_q, min(numq, max_q))
    #
    show_dimension_lines_bool = request.form.get("checkbox1") == "on"
    title_text = request.form.get("title_text", "")
    file_type = request.form.get("file_type", "pdf")
    mimetype = {"zip": "application/zip", "pdf": "application/pdf"}.get(file_type, "application/pdf")
    file = arearect.create_booklet_area_of_a_rectangle(numq, title_text, file_type=file_type, show_dimension_lines_bool=show_dimension_lines_bool)
    return send_file(file, as_attachment=True, mimetype=mimetype)


##########################################################################
# continue from here


@app.route("/dot_plots")
@app.route("/parallel_dot_plots")
@app.route("/parallel_overlay_dot_plots")
@app.route("/divided_bar_graphs")
@app.route("/pie_charts")
@app.route("/stem_leaf")
@app.route("/stem_leaf_back_to_back")
def coming_soon():
    """not yet developed pages"""
    """Renders the coming soon page for different routes"""
    # Extract the current route's endpoint name (the last part of the URL)
    page_name = request.path.split("/")[-1]

    return render_template("coming_soon.html", page_name=page_name)


##########################################################################
# clean up
##########################################################################


@app.after_request
def cleanup_after_request(response):
    """Cleanup any files not in current use; after any route call"""
    clean_output()
    return response


def add_cleanup_after_request():
    """Add cleanup task after the request to delete other files not in current use.
    Need to insert a line in each route call making files: add_cleanup_after_request()"""

    @after_this_request
    def after_request(response):
        clean_output()
        return response

    return after_request


# admin
def get_output_path():
    app_dir = Path(__file__).parent
    return app_dir / "output"


def remove_output_files(directory):
    """not use here yet"""
    # List of file extensions to remove
    file_extensions = ["*.tex", "*.pdf", "*.aux", "*fdb_latexmk", "*.fls", "*.log", "*.zip"]

    # standard_file_extensions = ["*.tex", "*.pdf"]
    # Iterate over each extension and remove matching files
    for ext in file_extensions:
        files = glob.glob(os.path.join(directory, ext))
        for file in files:
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")


@app.route("/clean_output")
def clean_output():
    remove_output_files(get_output_path())
    """Renders the clean_output page."""
    return render_template(
        "clean_output.html",
        title="Cleaned Output",
    )


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
