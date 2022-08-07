from django.urls import path
from .views import UploadImg

urlpatterns = [
    path("upload/", UploadImg.as_view(), name="load"),

]
