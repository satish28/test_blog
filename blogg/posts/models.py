from django.db import models
from django.contrib.auth.models import User

	
class UserPosts(models.Model):
    """
    User posts model
    """
    username = models.ForeignKey(User)
    first_name =  models.CharField(max_length=30)
    last_name =  models.CharField(max_length=30)	
    post_title = models.CharField(max_length=30)	
    post_content = models.TextField()	
    likes = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)
    created_timestamp = models.DateTimeField()