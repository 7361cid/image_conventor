from rest_framework import serializers
from .models import ImageModel


class ImgSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(max_length=None, use_url=False)

    class Meta:
        model = ImageModel
        fields = '__all__'
