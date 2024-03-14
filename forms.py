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



class ProfileForm(forms.Form):
    GENRE_CHOICES = (
        ('Jazz', 'Jazz'),
        ('Afro-Pop', 'Afro-Pop'),
        ('Funk-fusion', 'Funk-fusion'),
        ('R&B', 'R&B'),
        ('Soul', 'Soul'),
        ('Local', 'Local'),
        ('Rhumba', 'Rhumba'),
        ('Bongo', 'Bongo'),
        ('Gospel', 'Gospel'),
        ('Gengeton', 'Gengeton'),
        ('Benga', 'Benga'),
        ('Classical', 'Classical'),
        ('Rock', 'Rock'),
        ('Zilizopendwa', 'Zilizopendwa'),
        ('Pop', 'Pop'),
        ('Electronic', 'Electronic'),
        ('Country', 'Country'),
        ('Taarab', 'Taarab'),
        ('Mugithi', 'Mugithi'),
        ('Chakacha', 'Chakacha'),
        ('Reggaeton', 'Reggaeton'),
        ('Folk', 'Folk'),
        ('Indie', 'Indie'),
    )
    
    PROFESSION_CHOICES = (
    ('singer', 'Singer'),
    ('songwriter', 'Songwriter'),
    ('producer', 'Producer'),
    ('vocalist', 'Vocalist'),
    ('band', 'Band'),
    ('instrumentalist', 'Instrumentalist'),
    ('sound-engineer', 'Sound Engineer'),
    ('music-educator', 'Music Educator'),
    ('folk-traditional', 'Folk and Traditional'),
    ('dj', 'DJ'),
    ('cover-band', 'Cover Band'),
)

    SKILL_LEVEL_CHOICES = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('maestro', 'Maestro'),
)

    title = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=100)
    instagram = forms.URLField()
    facebook = forms.URLField()
    youtube = forms.URLField()
    genres = forms.MultipleChoiceField(choices=GENRE_CHOICES)  # Add your choices here
    profession = forms.ChoiceField(choices=PROFESSION_CHOICES)  # Add your choices here
    skill_level = forms.ChoiceField(choices=SKILL_LEVEL_CHOICES)  # Add your choices here
    charge_rate = forms.DecimalField()
    charge_rate_type = forms.ChoiceField(choices=[('Session', 'Per Session'), ('Hour', 'Per Hour')])  # Add more options if needed
    # samples = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    experience = forms.IntegerField()
    certifications = forms.FileField()
    profile_picture = forms.ImageField()


