from django.urls import path
from .views import UploadImg

urlpatterns = [
    path("", UploadImg.as_view(), name="load"),

]
