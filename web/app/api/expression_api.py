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
import json

from web.app.api import collections_api

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def submit_expression():
    expression = request.form["symbolic_expression"]

    parsed = parse_2_latex(expression)
    response_obj = compute_expression(parsed)
    response_obj_json = response_obj.to_json()

    collections_names,collections_infos = collections_api.get_collections()

    return render_template(
        "show_results.html",
        alert=False,
        query=expression,
        response_obj_json=response_obj_json,
        response_obj = response_obj,
        collections_names=collections_names,
        collections_infos=collections_infos
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