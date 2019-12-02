from django.urls import path

from .views import (
	encrypt_file, decrypt_file, file
)

app_name = 'abe'

urlpatterns = [
	path('encrypt',	encrypt_file, name='abe_encrypt'),
	path('decrypt',	decrypt_file, name='abe_decrypt'),
	path('file', file, name='file')
]
