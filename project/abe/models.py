from django.db import models


class UploadFileModel(models.Model):
	username = models.TextField()
	filename = models.TextField()
	content = models.TextField()
	and_attr = models.IntegerField()
	or_attr = models.IntegerField()
