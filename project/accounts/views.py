from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
	LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
)
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings

from .forms import (
	SignInViaUsernameForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm,
	SignUpForm, ChangeProfileForm, ChangeEmailForm,
)
from .models import Profile
# from django.contrib.auth.decorators import login_required

# @login_required(login_url='/accounts/login/')
class GuestOnlyView(View):
	def dispatch(self, request, *args, **kwargs):
		# Redirect to the index page if the user already authenticated
		if request.user.is_authenticated:
			return redirect(settings.LOGIN_REDIRECT_URL)

		return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
	template_name = 'accounts/log_in.html'

	@staticmethod
	def get_form_class(**kwargs):
		if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
			return SignInViaEmailForm

		if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
			return SignInViaEmailOrUsernameForm

		return SignInViaUsernameForm

	@method_decorator(sensitive_post_parameters('password'))
	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		# Sets a test cookie to make sure the user has cookies enabled
		request.session.set_test_cookie()

		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		request = self.request

		# If the test cookie worked, go ahead and delete it since its no longer needed
		if request.session.test_cookie_worked():
			request.session.delete_test_cookie()

		# The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
		# the SESSION_COOKIE_AGE settings' option.
		if settings.USE_REMEMBER_ME:
			if not form.cleaned_data['remember_me']:
				request.session.set_expiry(0)

		login(request, form.user_cache)

		redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
		url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

		if url_is_safe:
			return redirect(redirect_to)

		return redirect(settings.LOGIN_REDIRECT_URL)


class SignUpView(GuestOnlyView, FormView):
	template_name = 'accounts/sign_up.html'
	form_class = SignUpForm

	def form_valid(self, form):
		request = self.request
		user = form.save(commit=False)

		if settings.DISABLE_USERNAME:
			# Set a temporary username
			user.username = get_random_string()
		else:
			user.username = form.cleaned_data['username']

		if settings.ENABLE_USER_ACTIVATION:
			user.is_active = False

		# Create a user record
		user.save()

		# Change the username to the "user_ID" form
		if settings.DISABLE_USERNAME:
			user.username = f'user_{user.id}'
			user.save()

		act = Profile()
		act.user = user

		act.username = form.cleaned_data['username']
		act.first_name = form.cleaned_data['first_name']
		act.last_name = form.cleaned_data['last_name']
		act.email = form.cleaned_data['email']
		act.attr = 0
		for i in form.cleaned_data['attr']:
			act.attr += int(i)
		print(form.cleaned_data['attr'])

		act.save()

		raw_password = form.cleaned_data['password1']

		user = authenticate(username=user.username, password=raw_password)
		login(request, user)

		messages.success(request, _('You are successfully signed up!'))

		return redirect('index')


class UpdateProfileView(LoginRequiredMixin, FormView):
	template_name = 'accounts/profile/change_profile.html'


class ChangeProfileView(LoginRequiredMixin, FormView):
	template_name = 'accounts/profile/change_profile.html'
	form_class = ChangeProfileForm

	def get_initial(self):
		user = self.request.user
		initial = super().get_initial()
		initial['first_name'] = user.first_name
		initial['last_name'] = user.last_name
		return initial

	def form_valid(self, form):
		user = self.request.user
		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.save()

		messages.success(self.request, _('Profile data has been successfully updated.'))

		return redirect('accounts:change_profile')


class ChangeEmailView(LoginRequiredMixin, FormView):
	template_name = 'accounts/profile/change_email.html'
	form_class = ChangeEmailForm

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_initial(self):
		initial = super().get_initial()
		initial['email'] = self.request.user.email
		return initial

	def form_valid(self, form):
		user = self.request.user
		email = form.cleaned_data['email']

		user.email = email
		user.save()

		messages.success(self.request, _('Email successfully changed.'))

		return redirect('accounts:change_email')


class ChangePasswordView(BasePasswordChangeView):
	template_name = 'accounts/profile/change_password.html'

	def form_valid(self, form):
		# Change the password
		user = form.save()

		# Re-authentication
		login(self.request, user)

		messages.success(self.request, _('Your password was changed.'))

		return redirect('accounts:change_password')


class LogOutView(LoginRequiredMixin, BaseLogoutView):
	template_name = 'accounts/log_out.html'
