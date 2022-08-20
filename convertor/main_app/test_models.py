import os
import unittest
import PIL

from pathlib import Path
from django.core.files import File
from .models import ImageModel


class TestImageModel(unittest.TestCase):
    test_img = str(Path(__file__).parent) + r"\test_img.png"
    test_no_img = str(Path(__file__).parent) + r"\urls.py"

    def test_create_img_object(self):
        with open(self.test_img, "rb") as test_img:
            ImageModel.objects.create(format='jpeg', img=File(test_img, name=os.path.basename(test_img.name)))

    def test_convert_img(self):
        with open(self.test_img, "rb") as test_img:
            img = ImageModel.objects.create(format='jpeg', img=File(test_img, name=os.path.basename(test_img.name)))
            new_img, size = img.convert()
        self.assertEqual(size, (200, 200))
        self.assertEqual(new_img.split(".")[-1], "jpeg")

    def test_convert_no_img(self):
        with self.assertRaises(PIL.UnidentifiedImageError):
            with open(self.test_no_img, "rb") as test_no_img:
                img = ImageModel.objects.create(format='jpeg', img=File(test_no_img, name=os.path.basename(test_no_img.name)))
                img.convert()

    def test_convert_bad_format(self):
        with self.assertRaises(ValueError) as exc:
            with open(self.test_img, "rb") as test_img:
                img = ImageModel.objects.create(format='bad', img=File(test_img, name=os.path.basename(test_img.name)))
                img.convert()
        self.assertTrue('bad format' in str(exc.exception))


if __name__ == "__main__":
    unittest.main()
