from django.shortcuts import render
from django.contrib.auth.views import password_reset_confirm


def account_confirm(request, uidb64=None, token=None):
	return password_reset_confirm(
		request,
		template_name='account_confirmation_form.html',
		uidb64=uidb64,
		token=token,
		post_reset_redirect='/')
