from django.db import models
from django.contrib.auth.models import User

	
class UserPosts(models.Model):
    """
    User posts model
    """
    username = models.ForeignKey(User)
    post_title = models.CharField(max_length=100)	
    post_content = models.TextField()	
    likes = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.username.username + '-' + self.post_title
    
class UserPostLikes(models.Model):
    """
    User likes model
    """
    username = models.ForeignKey(User)
    post = models.ForeignKey(UserPosts)
    
    class Meta:
        unique_together = (('username', 'post'),)
        
    def __unicode__(self):
        return self.username.username + '-' + self.post.post_title

class UserPostCount(models.Model):
    """
    User post count
    """
    username = models.ForeignKey(User, unique=True)
    post_count = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.username.username + '-' + str(self.post_count)