import logging
import os

from flask import current_app, flash, jsonify, render_template, request
from werkzeug.utils import secure_filename

from web.app import limiter
from web.app.api.parser_api import exp2latex
from web.app.services.api_wolfram.waAPI import compute_expression
from web.app.services.web_services.user_services import UserService

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def rate_limit_from_config():
    appid = request.args.get("appid")
    username = request.args.get("username")
    if appid and username:
        return True
    else:
        return False


@limiter.limit("1 per day", exempt_when=rate_limit_from_config)
def solve_exp():
    exp = request.args.get("expression")
    pods_format = request.args.get("output")
    output_result = request.args.get("result")
    appid = request.args.get("appid")
    userid = request.args.get("userid")
    logging.info(UserService().check_appid(userid, appid))
    parsed = exp2latex(exp)
    solved = compute_expression(
        parsed, pods_format=pods_format, output_result=output_result
    )
    return jsonify({k: v for k, v in solved.__dict__.items() if k != "plots"})


def submit_expression():
    expression = request.form["symbolic_expression"]
    parsed = exp2latex(expression)
    response_obj = compute_expression(parsed)
    return render_template(
        "show_results.html",
        alert=False,
        query=expression,
        response_obj=response_obj,
    )


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
