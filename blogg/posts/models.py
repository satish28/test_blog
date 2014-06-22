from django.db import models
from login.models import MyUser

# Create your models here.

	
class UserPosts(models.Model):
	email = models.ForeignKey(MyUser)
	first_name =  models.CharField(max_length=30)
	last_name =  models.CharField(max_length=30)	
	post_title = models.CharField(max_length=30)	
	post_content = models.TextField()	
	likes = models.IntegerField(default=0)
	visits = models.IntegerField(default=0)
	created_timestamp = models.DateTimeField()
