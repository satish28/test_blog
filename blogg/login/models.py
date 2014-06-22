from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class MyUser(AbstractBaseUser):
	email = models.EmailField(max_length=254, unique=True, db_index=True, primary_key=True)
	firstname = models.CharField(max_length=50, null=False, blank=False)
	lastname = models.CharField(max_length=50, null=False, blank=True)
	
	USERNAME_FIELD = 'email'
