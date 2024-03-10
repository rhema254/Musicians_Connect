from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Musician
from django.contrib.auth.models import User
from django.forms import ModelForm

class RegistrationForm(ModelForm):
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


# class MusicianRegistrationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     username = forms.CharField(max_length=150, required=True)
#     email = forms.EmailField(required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True)
#     confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
#     date_of_birth = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1920, 2025)))

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords don't match")

#         # Add other validation checks as needed (e.g., username uniqueness, minimum age)
#         return cleaned_data

class MusicianForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = ['user', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple
        }



