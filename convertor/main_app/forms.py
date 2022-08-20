from django import forms
from .models import ImageModel


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ("img", "format")

    def clean(self):
        print(f"LOG form here")
        cleaned_data = super().clean()
        print(f"LOG form here {cleaned_data}")
        format = cleaned_data.get('format')
        img = cleaned_data.get('img')
        if format == str(img).split(".")[-1]:
            raise forms.ValidationError(f'Your choose same format {str(img).split(".")[-1]} ')
        else:
            return cleaned_data
