import os

from pathlib import Path
from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.files import File


class ApiTests(APITestCase):
    test_img = str(Path(__file__).parent) + f"{os.path.sep}test_img.png"

    def test_change_format(self):
        with open(self.test_img, "rb") as test_img:
            url = reverse("home") + "api/change_format/"
            data = {"format": "jpeg", "img": File(test_img)}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

    def test_resize(self):
        with open(self.test_img, "rb") as test_img:
            url = reverse("home") + "api/resize/"
            data = {"new_size": "100, 100", "img": File(test_img)}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

    def test_rotate(self):
        with open(self.test_img, "rb") as test_img:
            url = reverse("home") + "api/rotate/"
            data = {"degree": 45, "img": File(test_img)}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

    def test_crop(self):
        with open(self.test_img, "rb") as test_img:
            url = reverse("home") + "api/crop/"
            data = {"crop_coordinates": "100, 100, 200, 200", "img": File(test_img)}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

    def test_mirror(self):
        with open(self.test_img, "rb") as test_img:
            url = reverse("home") + "api/mirror/"
            data = {"img": File(test_img)}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)
