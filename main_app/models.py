import PIL

from PIL import Image
from django.db import models

FORMAT_CHOICES = (("png", "png"),
                  ("jpeg", "jpeg"),
                  ("bmp", "bmp"),
                  ("gif", "gif"),
                  ("ico", "ico"),
                  )


class ImageModel(models.Model):
    format = models.CharField(max_length=5, choices=FORMAT_CHOICES, default="jpeg", blank=True)
    img = models.ImageField(upload_to="images/")
    new_size = models.CharField(max_length=30, blank=True)
    degree = models.IntegerField(default=0, blank=True)
    crop_coordinates = models.CharField(max_length=50, blank=True)

    def convert(self, for_api=False):
        img = Image.open(self.img)
        rgb_img = img.convert('RGB')
        img_name = f"static/{str(self.img).split('.')[0]}.{self.format}"
        if self.format not in [f[0] for f in FORMAT_CHOICES]:
            raise ValueError("bad format")
        rgb_img.save(img_name, self.format)
        if for_api:
            return img_name
        else:
            return img_name, rgb_img.size

    def resize(self, for_api=False):
        img = Image.open(self.img)
        try:
            new_size = [int(i) for i in self.new_size.split(",")]
        except:
            raise ValueError("new_size")
        img = img.resize(new_size)
        img_name = f"static/{str(self.img)}"
        img.save(img_name)
        if for_api:
            return img_name
        else:
            return img_name, img.size

    def rotate(self, for_api=False):
        img = Image.open(self.img)
        if not str(self.degree).isdigit:
            raise ValueError("degree")
        img = img.rotate(int(self.degree))
        img_name = f"static/{str(self.img)}"
        img.save(img_name)
        if for_api:
            return img_name
        else:
            return img_name, img.size

    def crop(self, for_api=False):
        img = Image.open(self.img)
        try:
            crop_coordinates = [int(i) for i in self.crop_coordinates.split(",")]
        except:
            raise ValueError("crop_coordinates")
        if crop_coordinates[0] > img.size[0] or crop_coordinates[1] > img.size[1] or crop_coordinates[2] > img.size[0] or crop_coordinates[3] > img.size[1]:
            raise ValueError("crop_coordinates")
        img = img.crop(crop_coordinates)
        img_name = f"static/{str(self.img)}"
        img.save(img_name)
        if for_api:
            return img_name
        else:
            return img_name, img.size

    def mirror(self, for_api=False):
        img = Image.open(self.img)
        img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        img_name = f"static/{str(self.img)}"
        img.save(img_name)
        if for_api:
            return img_name
        else:
            return img_name, img.size
