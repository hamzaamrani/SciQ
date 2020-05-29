import logging
import os
import shutil
import zipfile

import cv2
import numpy as np

from web.app.config import OCR_CONFIG

from .model.img2seq import Img2SeqModel
from .model.utils.general import Config
from .model.utils.text import Vocab
from .utils import download_file_from_google_drive

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


class _OCRService():
    """
    Service serving OCR capability. It loads a OCR latex model to predict image characters
    """

    def __init__(self):
        # dir_output = OCR_CONFIG['model_dir']
        # if (not os.path.isdir(dir_output)):
        #     self._get_model_data()

        # config_vocab = Config(dir_output + "vocab.json")
        # config_model = Config(dir_output + "model.json")
        # vocab_path = os.path.join(dir_output, 'vocab.txt')
        # vocab = Vocab(config_vocab, vocab_path)

        # self.model = Img2SeqModel(config_model, dir_output, vocab)
        # self.model.build_pred()
        # self.model.restore_session(dir_output + "model.weights/")
        pass

    def _get_model_data(self, tmp_dir='./tmp'):
        os.makedirs(tmp_dir, exist_ok=True)
        path_to_zip_file = os.path.join(tmp_dir, 'tmp.zip')
        dir_output = OCR_CONFIG['model_dir']
        download_file_from_google_drive(OCR_CONFIG['drive_id'],
                                        path_to_zip_file)
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(dir_output)

        # shutil.rmtree(tmp_dir)

    def predict(self, img_path):
        """Translates an ASCIIMath string to LaTeX

        Args:
            img_path (str): path to (local) image to OCR

        Returns:
            str: LaTeX prediction of the input image
        """

        try:
            img = np.expand_dims(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), -1)
            hyps = self.model.predict(img)
            result = hyps[0]
            result = result.replace('\\,', '').replace(' ', '')
            logging.info(result)
            return result
        except Exception as ex:
            print("Are you kidding me?")
