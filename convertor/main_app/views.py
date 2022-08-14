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

    def post(self, request, *args, **kwargs):
        serializer = ImgSerializer(data=self.request.data)
        if serializer.is_valid():
            format = serializer.validated_data['format']
            img = serializer.validated_data['img']
            if format == str(img).split(".")[-1]:
                return Response("Same format", status=HTTPStatus.BAD_REQUEST)
            if str(img).split(".")[-1] not in ["bmp", "jpeg", "gif", "png", "ico"]:
                return Response("Bad file", status=HTTPStatus.BAD_REQUEST)
            if format not in ["bmp", "jpeg", "gif", "png", "ico"]:
                return Response("Bad format", status=HTTPStatus.BAD_REQUEST)
            img_obj = ImageModel.objects.create(format=format, img=img)
            img_obj.save()
            img = img_obj.convert(for_api=True)
            return Response({'img': img}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
