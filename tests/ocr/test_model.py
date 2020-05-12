import unittest
from web.app.services.ocr import OCRService

class TestOCRLoading(unittest.TestCase):

    def setUp(self):
        self.service = OCRService()

    def test_image(self):
        image_test = 'tests/ocr/images_test/hyp_0/0.png'
        self.service.predict(image_test)

if __name__ == "__main__":
    unittest.main()

