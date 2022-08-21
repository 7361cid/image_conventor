import os
import unittest
import PIL

from pathlib import Path
from django.core.files import File
from .models import ImageModel


class TestImageModel(unittest.TestCase):
    test_img = str(Path(__file__).parent) + f"{os.path.sep}test_img.png"
    test_no_img = str(Path(__file__).parent) + f"{os.path.sep}urls.py"

    def test_create_img_object(self):
        with open(self.test_img, "rb") as test_img:
            ImageModel.objects.create(format='jpeg', img=File(test_img, name=os.path.basename(test_img.name)))

    def test_change_format_img(self):
        with open(self.test_img, "rb") as test_img:
            img = ImageModel.objects.create(format='jpeg', img=File(test_img, name=os.path.basename(test_img.name)))
            new_img, size = img.convert()
        self.assertEqual(size, (200, 200))
        self.assertEqual(new_img.split(".")[-1], "jpeg")

    def test_change_format_no_img(self):
        with self.assertRaises(PIL.UnidentifiedImageError):
            with open(self.test_no_img, "rb") as test_no_img:
                img = ImageModel.objects.create(format='jpeg', img=File(test_no_img, name=os.path.basename(test_no_img.name)))
                img.convert()

    def test_change_format_bad_format(self):
        with self.assertRaises(ValueError) as exc:
            with open(self.test_img, "rb") as test_img:
                img = ImageModel.objects.create(format='bad', img=File(test_img, name=os.path.basename(test_img.name)))
                img.convert()
        self.assertTrue('bad format' in str(exc.exception))

    def test_resize_img(self):
        with open(self.test_img, "rb") as test_img:
            img = ImageModel.objects.create(new_size='100, 100', img=File(test_img, name=os.path.basename(test_img.name)))
            new_img, size = img.resize()
        self.assertEqual(size, (100, 100))

    def test_resize_img_bad_new_size(self):
        with self.assertRaises(ValueError) as exc:
            with open(self.test_img, "rb") as test_img:
                img = ImageModel.objects.create(new_size='bad',
                                                img=File(test_img, name=os.path.basename(test_img.name)))
                img.resize()
        self.assertTrue('new_size' in str(exc.exception))

    def test_rotate_img(self):
        with open(self.test_img, "rb") as test_img:
            img = ImageModel.objects.create(degree=45, img=File(test_img, name=os.path.basename(test_img.name)))
            img.rotate()

    def test_rotate_img_bad_new_size(self):
        with self.assertRaises(ValueError) as exc:
            with open(self.test_img, "rb") as test_img:
                img = ImageModel.objects.create(degree='bad',
                                                img=File(test_img, name=os.path.basename(test_img.name)))
                img.resize()
        self.assertTrue('degree' in str(exc.exception))

    def test_mirror_img(self):
        with open(self.test_img, "rb") as test_img:
            img = ImageModel.objects.create(img=File(test_img, name=os.path.basename(test_img.name)))
            img.mirror()

    def test_crop_img(self):
        with open(self.test_img, "rb") as test_img:
            img = ImageModel.objects.create(crop_coordinates="0, 0, 100, 100", img=File(test_img, name=os.path.basename(test_img.name)))
            img.crop()

    def test_crop_img_bad_coordinates(self):
        with self.assertRaises(ValueError) as exc:
            with open(self.test_img, "rb") as test_img:
                img = ImageModel.objects.create(crop_coordinates='bad',
                                                img=File(test_img, name=os.path.basename(test_img.name)))
                img.crop()
        self.assertTrue('crop_coordinates' in str(exc.exception))

    def test_crop_img_big_coordinates(self):
        with self.assertRaises(ValueError) as exc:
            with open(self.test_img, "rb") as test_img:
                img = ImageModel.objects.create(crop_coordinates='1000, 1000, 2000, 2000',
                                                img=File(test_img, name=os.path.basename(test_img.name)))
                img.crop()
        self.assertTrue('crop_coordinates' in str(exc.exception))


if __name__ == "__main__":
    unittest.main()
