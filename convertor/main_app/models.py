from PIL import Image
from django.db import models

FORMAT_CHOICES = (("png", "png"),
                  ("jpg", "jpg")
)


class ImageModel(models.Model):
    format = models.CharField(max_length=9, choices=FORMAT_CHOICES, default="jpg")
    img = models.ImageField(upload_to="images/profile/",)

    def convert(self):
        img = Image.open(self.img)
        img.convert('RGB').save(f"image_name.{self.format}", self.format)
        return img
