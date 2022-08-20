from django.urls import path, include
from rest_framework import routers
from .views import UploadImg, UploadImgAPI

router = routers.DefaultRouter()
router.register('convertor', UploadImgAPI, basename='img_load')

urlpatterns = [
    path("", UploadImg.as_view(), name="load"),
    path(r'api/', include(router.urls)),
]
