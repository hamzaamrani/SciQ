import logging
import os

from flask import current_app, flash, jsonify, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_optional
from flask_limiter.util import get_remote_address
from user_agents import parse
from web.app import LIMIT, limiter
from web.app.api import collections_api
from web.app.api.parser_api import exp2latex
from web.app.services.api_wolfram.waAPI import compute_expression
from web.app.services.utils.utils import exempt_limit, get_limit
from werkzeug.utils import secure_filename

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


@jwt_optional
@limiter.limit(get_limit, exempt_when=exempt_limit)
def solve_exp():
    if request.is_json:
        json = request.get_json()
        exp = None
        pods_format = None
        output_result = None
        if "expression" in json:
            exp = json["expression"]
        if "output" in json:
            pods_format = json["output"]
        if "result" in json:
            output_result = json["result"]
    else:
        exp = request.args.get("expression")
        pods_format = request.args.get("output")
        output_result = request.args.get("result")
    if exp is None:
        return jsonify({"error": "no expression to parse"})
    parsed = exp2latex(exp)
    solved = compute_expression(
        parsed, pods_format=pods_format, output_result=output_result
    )
    # logging.info(jsonify({k: v for k, v in solved.__dict__.items() if k != "plots"})
    return jsonify({k: v for k, v in solved.__dict__.items() if k != "plots"})


@jwt_optional
@limiter.limit(LIMIT, exempt_when=lambda: get_jwt_identity() is not None)
def submit_expression():
    logging.info(
        "Identita': "
        + str(get_jwt_identity())
        + " da IP: "
        + str(get_remote_address())
    )
    user_agent = parse(request.headers.get("User-Agent"))
    if user_agent.is_pc:
        try:
            logging.info("Requests from Desktop")
            expression = request.form["symbolic_expression"]
            parsed = exp2latex(expression)
            response_obj = compute_expression(parsed)
            response_obj_json = response_obj.to_json()
            (
                collections_names,
                collections_infos,
            ) = collections_api.get_collections()
            return render_template(
                "show_results.html",
                # query=expression,
                response_obj=response_obj,
                response_obj_json=response_obj_json,
                collections_names=collections_names,
                collections_infos=collections_infos,
            )
        except Exception as e:
            logging.info(e)
            return render_template(
                "math.html", alert=True, error="something goes wrong"
            )
    else:
        logging.info("Request from mobile")
        _json = request.get_json()
        expression = _json["symbolic_expression"]
        logging.info("Expression = " + expression)
        parsed = exp2latex(expression)
        response_obj = compute_expression(parsed).to_json()
        return jsonify(response_obj)


@jwt_optional
@limiter.limit(LIMIT, exempt_when=lambda: get_jwt_identity() is not None)
def send_file():
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
@limiter.exempt
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
