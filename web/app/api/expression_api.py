import logging
import os

from flask import (
    current_app,
    flash,
    jsonify,
    render_template,
    request,
)
from werkzeug.utils import secure_filename

from web.app.services.api_wolfram.waAPI import compute_expression
from web.app.services.parser.const import asciimath_grammar
from web.app.services.parser.parser import ASCIIMath2Tex

from web.app.services.api_wolfram.waAPI import Expression
import pickle

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def submit_expression():
    expression = request.form["symbolic_expression"]

    parsed = parse_2_latex(expression)
    response_obj = compute_expression(parsed)

    with open('tmp_expression', 'wb') as f:
        pickle.dump(response_obj, f)

    return render_template(
        "show_results.html",
        alert=False,
        query=expression,
        response_obj=response_obj,
    )


def parse_2_latex(expression):
    parser = ASCIIMath2Tex(
        asciimath_grammar, inplace=True, parser="lalr", lexer="contextual"
    )
    return parser.asciimath2tex(expression)


def send_file():
    logging.info("Current working location is = " + os.getcwd())
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    logging.info("Save path is = " + save_path)
    fileob.save(save_path)
    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass
    flash("File uploaded succesfully!")
    return "200"


# GET NAMES OF UPLOADED FILES
def get_filenames():
    logging.info("Current working location is = " + os.getcwd())
    filenames = os.listdir(current_app.config["UPLOAD_FOLDER"])

    def modify_time_sort(file_name):
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], file_name
        )
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)

# COLLECTIONS HANDLE
def save_expression_to_db():

    with open('tmp_expression', 'rb') as f:
        expression_obj = pickle.load(f)
    os.remove('tmp_expression')

    # expression_obj.print_expression()

    from web.app import mongo

    users = mongo.db.users
    id_user = "001"
    # qui id_user andrà letto dai token

    logging.info("Saving current expression to db...")

    # Check if user collection exists
    if users.find({ 'id_user': id_user } ).count() == 0:
        printer = {
                    'id_user' : id_user,
                    'expressions' : [],
                    'collections' : [
                        {
                            'default' : []
                        }
                    ]
                }

        users.insert_one(printer)
    
    users.update(
    { 'id_user' : id_user },
    {
        '$push': {
        'expressions': expression_obj.to_json()
        }
    }
    )

    logging.info("Saving expression to db has been completed with success!")

    return "okk"