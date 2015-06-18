from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import TimeclockUser


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = TimeclockUser
        fields = ('email',)


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TimeclockUser
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]
