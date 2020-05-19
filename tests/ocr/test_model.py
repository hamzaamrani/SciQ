import unittest
from web.app.services.ocr import _OCRService

class TestOCRLoading(unittest.TestCase):

    def setUp(self):
        self.service = _OCRService()

    def test_image(self):
        image_test = 'tests/ocr/images/1.png'
        self.service.predict(image_test)

if __name__ == "__main__":
    unittest.main()

