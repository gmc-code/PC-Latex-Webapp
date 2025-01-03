
from datetime import datetime
from flask import Flask, render_template,request,send_file
import latex.backtracking.backtracking_1step_booklet_maker as backtrack
import latex.backtracking.backtracking_2step_booklet_maker as backtrack2
import latex.numberlines.number_lines_booklet_maker as numline

app = Flask(__name__)


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

ops={'Addition':1,'Subtraction':2,'Multiplication':3,'Division':4, 'Random':5}
nlops={'Plus':1,'Minus Negative':2,'Minus':3,'Minus Positive':4, 'Plus Negative':5, 'Random':6}

@app.route('/')
def index():
    """Renders the home page."""
    return render_template(
        'home.html',
        title='Home Page',

    )

@app.route('/btonestep')
def btonestep():
    return render_template(
        'genform.html',
        title="One-Step Backtracking",
        ops=ops.keys(),
        link="/btonestepcreate",
    )

@app.route('/btonestepcreate')
def btonestepcreate():
    operation = ops[request.args.get('operation')]
    num_q=int(request.args.get('num_q'))
    file=backtrack.create_booklet(num_q,operation)
    return send_file(file, as_attachment=True)



@app.route('/bttwostep')
def bttwostep():
    return render_template(
        'genform2.html',
        title="Two-Step Backtracking",
        ops=ops.keys(),
        link="/bttwostepcreate",
    )

@app.route('/bttwostepcreate')
def bttwostepcreate():
    operation = ops[request.args.get('operation')]
    operation2= ops[request.args.get('operation2')]
    num_q=int(request.args.get('num_q'))
    file=backtrack2.create_booklet(num_q,operation,operation2)
    return send_file(file, as_attachment=True)

@app.route('/numberlines')
def numberlines():
    #"Enter 1,2,3,4,5 or 6 for plus,minus_neg,minus,minus_pos,plus_neg,random \n"
    return render_template(
        'genform.html',
        title="Numberlines",
        ops=nlops.keys(),
        link="/numberlinecreate",
    )

@app.route('/numberlinecreate')
def numberlinecreate():
    operation = nlops[request.args.get('operation')]
    num_q=int(request.args.get('num_q'))
    file=numline.create_booklet(num_q,operation)
    return send_file(file, as_attachment=True)



if __name__ == '__main__':
    # import os


    # HOST = os.environ.get('SERVER_HOST', 'localhost')
    # try:
    #     PORT = int(os.environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    app.run()
    # for ssl on https
    # app.run(ssl_context=('cert.pem', 'key.pem'))
