from rest_framework import serializers
from .models import ImageModel


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ["format", "img"]
