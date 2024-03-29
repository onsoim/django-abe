from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class UserCacheMixin:
	user_cache = None


class SignIn(UserCacheMixin, forms.Form):
	password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if settings.USE_REMEMBER_ME:
			self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

	def clean_password(self):
		password = self.cleaned_data['password']

		if not self.user_cache:
			return password

		if not self.user_cache.check_password(password):
			raise ValidationError(_('You entered an invalid password.'))

		return password


class SignInViaUsernameForm(SignIn):
	username = forms.CharField(label=_('Username'))

	@property
	def field_order(self):
		if settings.USE_REMEMBER_ME:
			return ['username', 'password', 'remember_me']
		return ['username', 'password']

	def clean_username(self):
		username = self.cleaned_data['username']

		user = User.objects.filter(username=username).first()
		if not user:
			raise ValidationError(_('You entered an invalid username.'))

		if not user.is_active:
			raise ValidationError(_('This account is not active.'))

		self.user_cache = user

		return username


class SignInViaEmailForm(SignIn):
	email = forms.EmailField(label=_('Email'))

	@property
	def field_order(self):
		if settings.USE_REMEMBER_ME:
			return ['email', 'password', 'remember_me']
		return ['email', 'password']

	def clean_email(self):
		email = self.cleaned_data['email']

		user = User.objects.filter(email__iexact=email).first()
		if not user:
			raise ValidationError(_('You entered an invalid email address.'))

		if not user.is_active:
			raise ValidationError(_('This account is not active.'))

		self.user_cache = user

		return email


class SignInViaEmailOrUsernameForm(SignIn):
	email_or_username = forms.CharField(label=_('Email or Username'))

	@property
	def field_order(self):
		if settings.USE_REMEMBER_ME:
			return ['email_or_username', 'password', 'remember_me']
		return ['email_or_username', 'password']

	def clean_email_or_username(self):
		email_or_username = self.cleaned_data['email_or_username']

		user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
		if not user:
			raise ValidationError(_('You entered an invalid email address or username.'))

		if not user.is_active:
			raise ValidationError(_('This account is not active.'))

		self.user_cache = user

		return email_or_username


class UpdateProfileForm(forms.Form):
	first_name = forms.CharField(label=_('First name'), max_length=30, required=False)
	last_name = forms.CharField(label=_('Last name'), max_length=150, required=False)
	


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = settings.SIGN_UP_FIELDS

	email = forms.EmailField(label=_('Email'), help_text=_('Required. Enter an existing email address.'))
	attr = forms.MultipleChoiceField(label=_('Attr'), choices=[
			(0x01 << 0x0,'Employee'),
			(0x01 << 0x1,'Team Leader'),
			(0x01 << 0x2,'Project Manager'),
			(0x01 << 0x3,'Assistant Project'),
			(0x01 << 0x4,'Managerer'),
			(0x01 << 0x5,'Admin'),
			(0x01 << 0x6,'NonEmployee'),
			(0x01 << 0x7,'Unregistered'),
			(0x01 << 0x8,'Registered'),
			(0x01 << 0x9,'student'),
			(0x01 << 0xa,'Trainee'),
			(0x01 << 0xb,'HR'),
		], widget=forms.CheckboxSelectMultiple)

	def clean_email(self):
		email = self.cleaned_data['email']

		user = User.objects.filter(email__iexact=email).exists()
		if user:
			raise ValidationError(_('You can not use this email address.'))

		return email


class ChangeProfileForm(forms.Form):
	first_name = forms.CharField(label=_('First name'), max_length=30, required=False)
	last_name = forms.CharField(label=_('Last name'), max_length=150, required=False)


class ChangeEmailForm(forms.Form):
	email = forms.EmailField(label=_('Email'))

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super().__init__(*args, **kwargs)

	def clean_email(self):
		email = self.cleaned_data['email']

		if email == self.user.email:
			raise ValidationError(_('Please enter another email.'))

		user = User.objects.filter(Q(email__iexact=email) & ~Q(id=self.user.id)).exists()
		if user:
			raise ValidationError(_('You can not use this mail.'))

		return email
