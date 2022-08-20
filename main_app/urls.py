from django.urls import path, include
from rest_framework import routers
from .views import MainView, ChangeFormatImg, ChangeFormatImgAPI, ResizeImg

router = routers.DefaultRouter()
router.register('convertor', ChangeFormatImgAPI, basename='img_load')

urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("/change_format/", ChangeFormatImg.as_view(), name="change_format"),
    path("/resize/", ResizeImg.as_view(), name="resize"),
    path(r'api/', include(router.urls)),
]
