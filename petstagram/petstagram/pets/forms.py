from django import forms

from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_name', 'pet_birth', 'pet_photo']

        widgets = {
            'pet_name': forms.TextInput(attrs={'placeholder': "Enter your pet's name"}),
            'pet_birth': forms.DateInput(attrs={'type': 'date'}),
            'pet_photo': forms.TextInput(attrs={'placeholder': 'Link to image'}),
        }

        labels = {
            'pet_birth': 'Date of Birth',
            'pet_photo': 'Link to Image',
        }


class PetDeleteForm(PetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'