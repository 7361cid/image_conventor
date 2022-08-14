from PIL import Image
from django.db import models

FORMAT_CHOICES = (("png", "png"),
                  ("jpeg", "jpeg"),
                  ("bmp", "bmp"),
                  ("gif", "gif"),
                  ("ico", "ico"),
                  )


class ImageModel(models.Model):
    format = models.CharField(max_length=9, choices=FORMAT_CHOICES, default="jpeg")
    img = models.ImageField(upload_to="images/before_convert/", )

    def convert(self, for_api=False):
        img = Image.open(self.img)
        rgb_img = img.convert('RGB')
        img_name = f"static/{str(self.img).split('.')[0]}.{self.format}"
        rgb_img.save(img_name, self.format)
        if for_api:
            with open(img_name, 'rb') as f:
                return str(f.read())
        else:
            return img_name, rgb_img.size
