import os
import unittest

from pathlib import Path
from django.core.files import File
from .models import ImageModel


class TestImageModel(unittest.TestCase):
    test_img = str(Path(__file__).parent) + r"\test_img.png"

    def test_create_img_object(self):
        with open(self.test_img, "rb") as test_img:
            ImageModel.objects.create(format='jpeg', img=File(test_img, name=os.path.basename(test_img.name)))


if __name__ == "__main__":
    unittest.main()
