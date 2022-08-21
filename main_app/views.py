from django.views.generic.edit import FormView
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from django.shortcuts import render
from django.views.generic.base import TemplateView
from http.server import HTTPStatus
from .forms import ChangeFormatForm, ResizeImgForm, RotateImgForm, CropImgForm, MirrorImgForm
from .models import ImageModel
from .serializers import ImgSerializer


class MainView(TemplateView):
    template_name = 'main.html'


class ChangeFormatImg(FormView):
    template_name = 'load_img.html'
    form_class = ChangeFormatForm
    success_url = '/'

    def form_valid(self, form):
        context = {}
        if form.data['format'] and "img" in self.request.FILES.keys():
            img_obj = ImageModel.objects.create(format=form.data['format'], img=self.request.FILES['img'])
            img_obj.save()
            img_name, size = img_obj.convert()
            context['img'] = img_name
            context['size'] = size
        return render(self.request, 'get_result.html', context)


class ResizeImg(FormView):
    template_name = 'load_img.html'
    form_class = ResizeImgForm
    success_url = '/'

    def form_valid(self, form):
        context = {}
        if form.data['new_size'] and "img" in self.request.FILES.keys():
            img_obj = ImageModel.objects.create(new_size=form.data['new_size'], img=self.request.FILES['img'])
            img_obj.save()
            img_name, size = img_obj.resize()
            context['img'] = img_name
            context['size'] = size
        return render(self.request, 'get_result.html', context)


class RotateImg(FormView):
    template_name = 'load_img.html'
    form_class = RotateImgForm
    success_url = '/'

    def form_valid(self, form):
        context = {}
        if form.data['degree'] and "img" in self.request.FILES.keys():
            img_obj = ImageModel.objects.create(degree=form.data['degree'], img=self.request.FILES['img'])
            img_obj.save()
            img_name, size = img_obj.rotate()
            context['img'] = img_name
            context['size'] = size
        return render(self.request, 'get_result.html', context)


class CropImg(FormView):
    template_name = 'load_img.html'
    form_class = CropImgForm
    success_url = '/'

    def form_valid(self, form):
        context = {}
        if form.data['crop_coordinates'] and "img" in self.request.FILES.keys():
            img_obj = ImageModel.objects.create(crop_coordinates=form.data['crop_coordinates'], img=self.request.FILES['img'])
            img_obj.save()
            img_name, size = img_obj.crop()
            context['img'] = img_name
            context['size'] = size
        return render(self.request, 'get_result.html', context)


class MirrorImg(FormView):
    template_name = 'load_img.html'
    form_class = MirrorImgForm
    success_url = '/'

    def form_valid(self, form):
        context = {}
        if "img" in self.request.FILES.keys():
            img_obj = ImageModel.objects.create(img=self.request.FILES['img'])
            img_obj.save()
            img_name, size = img_obj.mirror()
            context['img'] = img_name
            context['size'] = size
        return render(self.request, 'get_result.html', context)


class ChangeFormatImgAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ImgSerializer
    queryset = ImageModel.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = ImgSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                format = serializer.validated_data['format']
            except KeyError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            img = serializer.validated_data['img']
            if format == str(img).split(".")[-1]:
                return Response("Same format", status=HTTPStatus.BAD_REQUEST)
            if str(img).split(".")[-1] not in ["bmp", "jpeg", "gif", "png", "ico"]:
                return Response("Bad file", status=HTTPStatus.BAD_REQUEST)
            if format not in ["bmp", "jpeg", "gif", "png", "ico"]:
                return Response("Bad format", status=HTTPStatus.BAD_REQUEST)
            img_obj = ImageModel.objects.create(format=format, img=img)
            img_obj.save()
            try:
                img = img_obj.convert(for_api=True)
            except ValueError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            return Response({'img_url': img}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class ResizeImgAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ImgSerializer
    queryset = ImageModel.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = ImgSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                new_size = serializer.validated_data['new_size']
            except KeyError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            img = serializer.validated_data['img']
            img_obj = ImageModel.objects.create(new_size=new_size, img=img)
            img_obj.save()
            try:
                img = img_obj.resize(for_api=True)
            except ValueError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            return Response({'img_url': img}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class RotateImgAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ImgSerializer
    queryset = ImageModel.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = ImgSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                degree = serializer.validated_data['degree']
            except KeyError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            img = serializer.validated_data['img']
            img_obj = ImageModel.objects.create(degree=degree, img=img)
            img_obj.save()
            try:
                img = img_obj.rotate(for_api=True)
            except ValueError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            return Response({'img_url': img}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class CropImgAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ImgSerializer
    queryset = ImageModel.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = ImgSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                crop_coordinates = serializer.validated_data['crop_coordinates']
            except KeyError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            img = serializer.validated_data['img']
            img_obj = ImageModel.objects.create(crop_coordinates=crop_coordinates, img=img)
            img_obj.save()
            try:
                img = img_obj.crop(for_api=True)
            except ValueError as err:
                return Response(str(err), status=HTTPStatus.BAD_REQUEST)
            return Response({'img_url': img}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class MirrorImgAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ImgSerializer
    queryset = ImageModel.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = ImgSerializer(data=self.request.data)
        if serializer.is_valid():
            img = serializer.validated_data['img']
            img_obj = ImageModel.objects.create(img=img)
            img_obj.save()
            img = img_obj.mirror(for_api=True)
            return Response({'img_url': img}, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
