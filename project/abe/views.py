from django.shortcuts import render
from .forms import UploadFileForm
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import UploadFileModel
from accounts.models import Profile

def attr2int(attrs):
	attrs_list = ['Employee','Team_Leader','Project_Manager','Assistant_Project','Managerer','Admin','NonEmployee','Unregistered','Registered','student','Trainee','HR']
	sum = 0
	for attr in attrs:
		try:
			sum += (0x01 << attrs_list.index(attr))
			print(f'{sum}, {attr}')
		except: pass
	return sum


def encrypt_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		enc = form.save(commit=False)
		enc.username	= request.user.username
		enc.filename	= request.POST['filename']
		enc.content		= request.POST['crpyted_content']
		enc.and_attr	= int(request.POST['and_op'],10)
		enc.or_attr		= int(request.POST['or_op'],10)
		enc.save()
		messages.success(request, _(f'You are successfully uploaded [ {request.POST["filename"]} ]!'))

	form = UploadFileForm()
	return render(request, 'abe/encryption.html', {'form': form})


def decrypt_file(request):
	boardList = UploadFileModel.objects.order_by('id')
	return render(request, 'abe/decryption.html', {'boardList': boardList})


def file(request):
	file = UploadFileModel.objects.get(id=request.GET['id'])
	attr = Profile.objects.get(username=request.user.username).attr
	return render(request, 'abe/file.html', {'id': id, 'file':file, 'attr':attr})