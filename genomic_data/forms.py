from django import forms
from .models import GenomicData

class GenomicDataForm(forms.ModelForm):
    class Meta:
        model = GenomicData
        fields = ['title', 'description', 'data_file']

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
from django import forms
from .models import GenomicData
from django.contrib.auth.models import User

class ShareDataForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    data_file = forms.FileField(required=True)

    class Meta:
        model = GenomicData
        fields = ['data_file', 'title', 'description', 'users']

from django import forms
from django.contrib.auth.models import User

class UserSettingsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)  # Pour permettre la modification du mot de passe

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Seules ces informations peuvent être modifiées

