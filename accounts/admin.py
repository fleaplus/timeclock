from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.utils.crypto import get_random_string

from .models import TimeclockUser


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = TimeclockUser
        fields = ('email',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TimeclockUser
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


class TimeclockUserAdmin(UserAdmin):
    add_form_template = 'add_form.html'
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super(TimeclockUserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            if reset_form.is_valid():
                reset_form.save(
                    request=request,
                    use_https=request.is_secure(),
                    subject_template_name='account_creation_subject.txt',
                    email_template_name='account_creation_email.html')

admin.site.register(TimeclockUser, TimeclockUserAdmin)
