from PIL import Image
from django.db import models

FORMAT_CHOICES = (("png", "png"),
                  ("jpeg", "jpeg"),
                  ("bmp", "bmp"),
                  ("gif", "gif"),
                  ("ico", "ico"),
                  )


# BMP, EPS, GIF, IM, JPEG, MSP, PCX PNG, PPM, TIFF, WebP, ICO
class ImageModel(models.Model):
    format = models.CharField(max_length=9, choices=FORMAT_CHOICES, default="jpeg")
    img = models.ImageField(upload_to="images/before_convert/", )

    def convert(self):
        img = Image.open(self.img)
        print(f"LOG {self.format} --- {self.img} --- {self.img.name}  ")
        rgb_img = img.convert('RGB')
        img_name = f"static/{str(self.img).split('.')[0]}.{self.format}"
        rgb_img.save(img_name, self.format)
        return img_name
