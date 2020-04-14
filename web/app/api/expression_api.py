from flask import request
import hashlib
from flask import abort, redirect, url_for, render_template, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from web.app.services import user_services
from flask import current_app
import os
import json
import logging
from web.app.services.api_wolfram.waAPI import Expression, compute_expression

from web.app.services.parser.parser import ASCIIMath2Tex
from web.app.services.parser.const import asciimath_grammar

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def submit_expression():
    expression = request.form["symbolic_expression"]
    parsed = parse_2_latex(expression)
    response_obj = compute_expression(parsed)
    response_obj.print_expression()
    return render_template("show_results.html", alert=False, query=expression, response_obj= response_obj)


def parse_2_latex(expression):
    parser = ASCIIMath2Tex(asciimath_grammar,
                           inplace=True,
                           parser="lalr",
                           lexer="contextual")
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
    filenames = os.listdir(current_app.config['UPLOAD_FOLDER'])

    def modify_time_sort(file_name):
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time
    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)
