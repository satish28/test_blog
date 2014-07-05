from django import forms
from posts.models import UserPosts

class UserPostForm(forms.ModelForm):
	post_title = forms.CharField(max_length=30, help_text="Please enter the title")
	post_content = forms.CharField(widget=forms.Textarea)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	visits = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	created_timestamp = forms.DateField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = UserPosts
		fields=('username','post_title','post_content','likes','visits','created_timestamp')
		exclude=('username',)
