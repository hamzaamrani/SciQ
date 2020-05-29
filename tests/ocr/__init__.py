import os
from os import path
os.environ["MODEL_DIR"] = path.join(path.curdir, "tests", "ocr", "model")
