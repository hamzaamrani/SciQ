import hashlib
import os

from flask import current_app, flash, render_template, request
from werkzeug.utils import secure_filename

from web.app.services.ocr import OCR_SERVICE


def ocr():
    try:
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

        result = OCR_SERVICE.predict(save_path)

        return result
    except ValueError as valerr:
        flash(valerr)
