import os

from pathlib import Path
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files import File


class TestViews(TestCase):
    test_img = str(Path(__file__).parent) + f"{os.path.sep}test_img.png"

    def test_change_format_view_get(self):
        client = Client()
        response = client.get(reverse("change_format"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "load_img.html")

    def test_change_format_view_post(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"format": "jpeg", "img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("change_format"), data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "get_result.html")

    def test_change_format_view_post_no_img(self):
        client = Client()
        data = {"format": "jpeg"}
        response = client.post(reverse("change_format"), data)
        self.assertFormError(response, 'form', 'img', 'This field is required.')

    def test_view_post_no_format(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("change_format"), data)
            self.assertFormError(response, 'form', 'format', 'This field is required.')

    def test_resize_view_get(self):
        client = Client()
        response = client.get(reverse("resize"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "load_img.html")

    def test_resize_view_post(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"new_size": "100, 100", "img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("resize"), data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "get_result.html")

    def test_resize_view_post_no_img(self):
        client = Client()
        data = {"new_size": "100, 100"}
        response = client.post(reverse("resize"), data)
        self.assertFormError(response, 'form', 'img', 'This field is required.')

    def test_resize_view_post_no_new_size(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("resize"), data)
            self.assertFormError(response, 'form', 'new_size', 'This field is required.')

    def test_rotate_view_get(self):
        client = Client()
        response = client.get(reverse("rotate"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "load_img.html")

    def test_rotate_view_post(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"degree": 45, "img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("rotate"), data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "get_result.html")

    def test_rotate_view_post_no_img(self):
        client = Client()
        data = {"degree": 45}
        response = client.post(reverse("rotate"), data)
        self.assertFormError(response, 'form', 'img', 'This field is required.')

    def test_rotate_view_post_no_degree(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("rotate"), data)
            self.assertFormError(response, 'form', 'degree', 'This field is required.')

    def test_crop_view_get(self):
        client = Client()
        response = client.get(reverse("crop"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "load_img.html")

    def test_crop_view_post(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"crop_coordinates": "100, 100, 200, 200", "img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("crop"), data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "get_result.html")

    def test_crop_view_post_no_img(self):
        client = Client()
        data = {"crop_coordinates": "100, 100, 200, 200"}
        response = client.post(reverse("crop"), data)
        self.assertFormError(response, 'form', 'img', 'This field is required.')

    def test_crop_view_post_no_coordinates(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("crop"), data)
            self.assertFormError(response, 'form', 'crop_coordinates', 'This field is required.')

    def test_mirror_view_get(self):
        client = Client()
        response = client.get(reverse("mirror"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "load_img.html")

    def test_mirror_view_post(self):
        with open(self.test_img, "rb") as test_img:
            client = Client()
            data = {"img": File(test_img, name=os.path.basename(test_img.name))}
            response = client.post(reverse("mirror"), data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "get_result.html")

    def test_mirror_view_post_no_img(self):
        client = Client()
        data = {}
        response = client.post(reverse("crop"), data)
        self.assertFormError(response, 'form', 'img', 'This field is required.')
