import logging
from web.app.config import OCR_CONFIG
import cv2
import numpy as np
from .model.img2seq import Img2SeqModel
from .model.utils.general import Config, run
from .model.utils.text import Vocab
from .utils import download_file_from_google_drive
import zipfile
import os
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

class OCRService():
    """
    Service serving OCR capability
    """
    
    def __init__(self):
        dir_output = OCR_CONFIG['model_dir']
        if (not os.path.isdir(dir_output)):
            self._get_model_data()

        config_vocab = Config(dir_output + "vocab.json")
        config_model = Config(dir_output + "model.json")
        vocab_path = os.path.join(dir_output, 'vocab.txt')
        vocab = Vocab(config_vocab, vocab_path)
        
        self.model = Img2SeqModel(config_model, dir_output, vocab)
        self.model.build_pred()
        self.model.restore_session(dir_output + "model.weights/")
        
    def _get_model_data(self, tmp_dir='./tmp'):
        os.makedirs(tmp_dir, exist_ok=True)
        path_to_zip_file = os.path.join(tmp_dir, 'tmp.zip')
        dir_output = OCR_CONFIG['model_dir']
        download_file_from_google_drive(OCR_CONFIG['drive_id'],
                                        path_to_zip_file)
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(dir_output)

        
    def predict(self, img_path):
        """
        Predict latex from image
        """
        try:
            breakpoint()
            img = np.expand_dims(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), -1)
            hyps = self.model.predict(img)
            logging.info(hyps[0])
            return hyps

        except:
            print("Are you kidding me?")
                
                













        
