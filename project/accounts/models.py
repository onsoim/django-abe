from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	username = models.CharField(max_length=150)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=150)

	email = models.EmailField(blank=True)
	attr = models.IntegerField()


# class UserProfile(AbstractUser):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	CHOICE_GENDER = (
# 		('M', 'Male'),
# 		('F', 'Female'),
# 		('O', 'Other'),
# 	)
# 	gender = models.CharField(max_length=1, choices=CHOICE_GENDER)

# 	def __str__(self):
# 		return self.username
