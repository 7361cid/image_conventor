from django.views.generic.edit import FormView
from django.shortcuts import render
from .forms import ImageForm
from .models import ImageModel


class UploadImg(FormView):
    template_name = 'load_img.html'
    form_class = ImageForm
    success_url = '/'

    def form_valid(self, form):
        context = {}
        print(f"here {form}")
        if form.data['format'] and "img" in self.request.FILES.keys():
            img_obj = ImageModel.objects.create(format=form.data['format'], img=self.request.FILES['img'])
            img_obj.save()
            context['img'] = img_obj.convert()
        return render(self.request, 'get_result.html', context)
