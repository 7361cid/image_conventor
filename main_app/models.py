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
    img = models.ImageField(upload_to="images/before_convert/")
    new_size = models.CharField(max_length=30, blank=True)

    def convert(self, for_api=False):
        img = Image.open(self.img)
        rgb_img = img.convert('RGB')
        img_name = f"static/{str(self.img).split('.')[0]}.{self.format}"
        if self.format not in [f[0] for f in FORMAT_CHOICES]:
            raise ValueError("bad format")
        rgb_img.save(img_name, self.format)
        if for_api:
            with open(img_name, 'rb') as f:
                return str(f.read())
        else:
            return img_name, rgb_img.size

    def resize(self):
        img = Image.open(self.img)
        print(f"resize {self.new_size} type {type(self.new_size)}")
        new_size = [int(i) for i in self.new_size.split(",")]
        img = img.resize(new_size)
        img_name = f"static/{str(self.img)}"
        img.save(img_name)
        print(f"resize {img.size}")
        return img_name, img.size
