import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

def get_image_path(instance, filename):
	return os.path.join('users', str(instance.id), filename)

class FestivalAdvisorUser(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
	picture = models.ImageField(verbose_name='Profielafbeelding', upload_to=get_image_path, blank=True, null=True)
	gender = models.CharField(max_length=27, blank=True, null=True)
	age_min = models.PositiveIntegerField(blank=True, null=True)
	age_max = models.PositiveIntegerField(blank=True, null=True)

	def __str__(self):

		return self.user.username