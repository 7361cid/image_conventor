from django import forms
from .models import ImageModel


class ChangeFormatForm(forms.ModelForm):
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


class ResizeImgForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ("img", "new_size")

    def clean(self):
        print(f"LOG form here")
        cleaned_data = super().clean()
        print(f"LOG form here {cleaned_data}")
        new_size = cleaned_data.get('new_size')
        try:
            new_size = new_size.split(",")
            print(f"LOG form here2 {new_size}")
            if len(new_size) != 2:
                raise forms.ValidationError(f' Enter right size ')
            print(f"LOG form here3 {new_size}")
            if not new_size[0].strip().isdigit() or not new_size[1].strip().isdigit():
                raise forms.ValidationError(f' Enter numbers ')
            print(f"LOG form here4 {new_size}")
        except:
            raise forms.ValidationError(f' new size must be in format number, number ')
        else:
            return cleaned_data
