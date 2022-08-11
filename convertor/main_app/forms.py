from django import forms
from .models import ImageModel


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ("img", "format")

    def clean_format(self):
        format = self.cleaned_data.get('format')
        """ this will give you the actual username from the field
            Now you may get that validated
        """
        img = self.cleaned_data.get('img')
        if img is None:
            return forms.ValidationError("Choose file before format")
        elif format == str(img).split(".")[-1]:
            return forms.ValidationError(f'Your choose same format {str(img).split(".")[-1]} ')
        else:
            return format
