from django import forms
from posts.models import UserPosts

class UserPostForm(forms.ModelForm):
	post_title = forms.CharField(max_length=100, help_text="Please enter the title")
	post_content = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = UserPosts
		fields=('post_title','post_content')
