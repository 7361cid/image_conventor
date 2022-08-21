from django.urls import path, include
from rest_framework import routers
from .views import MainView, ChangeFormatImg, ResizeImg, RotateImg, CropImg, MirrorImg, ChangeFormatImgAPI, \
    ResizeImgAPI, RotateImgAPI, CropImgAPI, MirrorImgAPI


router = routers.DefaultRouter()
router.register('change_format', ChangeFormatImgAPI, basename='api_change_format')
router.register('resize', ResizeImgAPI, basename='api_resize')
router.register('rotate', RotateImgAPI, basename='api_rotate')
router.register('crop', CropImgAPI, basename='api_crop')
router.register('mirror', MirrorImgAPI, basename='api_mirror')

urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("/change_format/", ChangeFormatImg.as_view(), name="change_format"),
    path("/resize/", ResizeImg.as_view(), name="resize"),
    path("/rotate/", RotateImg.as_view(), name="rotate"),
    path("/crop/", CropImg.as_view(), name="crop"),
    path("/mirror/", MirrorImg.as_view(), name="mirror"),
    path(r'api/', include(router.urls), name="api"),
]
