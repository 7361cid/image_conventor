from django import forms
from .models import ImageModel


class ChangeFormatForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ("img", "format")

    def __init__(self, *args, **kwargs):
        super(ChangeFormatForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    def clean(self):
        cleaned_data = super().clean()
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

    def __init__(self, *args, **kwargs):
        super(ResizeImgForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    def clean(self):
        cleaned_data = super().clean()
        new_size = cleaned_data.get('new_size')
        try:
            new_size = new_size.split(",")
            if len(new_size) != 2:
                raise forms.ValidationError(f' Enter right size ')
            if not new_size[0].strip().isdigit() or not new_size[1].strip().isdigit():
                raise forms.ValidationError(f' Enter numbers ')
        except:
            raise forms.ValidationError(f' new size must be in format number, number ')
        else:
            return cleaned_data


class RotateImgForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ("img", "degree")

    def __init__(self, *args, **kwargs):
        super(RotateImgForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    def clean(self):
        cleaned_data = super().clean()
        degree = cleaned_data.get('degree')
        try:
            if not isinstance(degree, int):
                raise forms.ValidationError(f' degree must be a number ')
        except:
            raise forms.ValidationError(f' degree must be a number ')
        else:
            return cleaned_data


class CropImgForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ("img", "crop_coordinates")

    def __init__(self, *args, **kwargs):
        super(CropImgForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    def clean(self):
        cleaned_data = super().clean()
        crop_coordinates = cleaned_data.get('crop_coordinates')
        try:
            crop_coordinates = crop_coordinates.split(",")
            if len(crop_coordinates) != 4:
                raise forms.ValidationError(f' Enter coordinates in format x1, x2, y1, y2 ')
            for coord in crop_coordinates:
                if not coord.strip().isdigit():
                    raise forms.ValidationError(f' Enter numbers ')
        except:
            raise forms.ValidationError(f' Enter coordinates in format x1, x2, y1, y2 ')
        else:
            return cleaned_data


class MirrorImgForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ("img",)

    def __init__(self, *args, **kwargs):
        super(MirrorImgForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
