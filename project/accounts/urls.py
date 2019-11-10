from django.urls import path

from .views import (
	LogInView, SignUpView, LogOutView, UpdateProfileView,
	ChangeEmailView, ChangeProfileView, ChangePasswordView,
)

app_name = 'accounts'

urlpatterns = [
	path('login/', LogInView.as_view(), name='log_in'),
	path('signup/', SignUpView.as_view(), name='sign_up'),

	path('logout/', LogOutView.as_view(), name='log_out'),

	path('update', UpdateProfileView.as_view(), name='update'),

	path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
	path('change/password/', ChangePasswordView.as_view(), name='change_password'),
	path('change/email/', ChangeEmailView.as_view(), name='change_email'),
]
