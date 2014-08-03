from django.contrib import admin
from posts.models import UserPosts, UserPostLikes, UserPostCount

admin.site.register(UserPosts)
admin.site.register(UserPostLikes)
admin.site.register(UserPostCount)