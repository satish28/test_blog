from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
	email = models.EmailField(max_length=254, unique=True, db_index=True, primary_key=True)
	first_name = models.CharField(max_length=50, null=False, blank=False)
	last_name = models.CharField(max_length=50, null=False, blank=True)
	
	USERNAME_FIELD = 'email'
