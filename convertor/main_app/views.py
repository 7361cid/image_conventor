from django.views.generic.edit import FormView
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from django.shortcuts import render
from http.server import HTTPStatus
from .forms import ImageForm
from .models import ImageModel
from .serializers import ImgSerializer


class UploadImg(FormView):
    template_name = 'load_img.html'
    form_class = ImageForm
    success_url = '/'

    def form_valid(self, form):
        context = {}
        if form.data['format'] and "img" in self.request.FILES.keys():
            img_obj = ImageModel.objects.create(format=form.data['format'], img=self.request.FILES['img'])
            img_obj.save()
            img_name, size = img_obj.convert()
            context['img'] = img_name
            context['size'] = size
        print(f"Log size {size}")
        return render(self.request, 'get_result.html', context)


class UploadImgAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ImgSerializer
    queryset = ImageModel.objects.all()

    def get(self, request, *args, **kwargs):
        return Response({'format': "format"}, status=HTTPStatus.OK)

    def post(self, request, *args, **kwargs):
        serializer = ImgSerializer(data=self.request.data)
        if serializer.is_valid():
            print(f"LOG API {serializer}")
            format = serializer.validated_data['format']
            return Response({'format': format}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
