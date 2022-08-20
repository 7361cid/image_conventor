import os

from pathlib import Path
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files import File


class TestUploadImgView(TestCase):
    test_img = str(Path(__file__).parent) + f"{os.path.sep}test_img.png"

    def test_view_get(self):
        client = Client()
        response = client.get(reverse("load"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "load_img.html")

    def test_view_post(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"format": "jpeg", "img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("load"), data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "get_result.html")

    def test_view_post_no_img(self):
        client = Client()
        data = {"format": "jpeg"}
        response = client.post(reverse("load"), data)
        print(f"Log res {response.content}")
        self.assertFormError(response, 'form', 'img', 'This field is required.')

    def test_view_post_no_format(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("load"), data)
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'format', 'This field is required.')
