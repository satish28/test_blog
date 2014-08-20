from django import forms
from posts.models import UserPosts

class UserPostForm(forms.ModelForm):
	post_title = forms.CharField(max_length=100, help_text="Please enter the title")
	post_content = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = UserPosts
		fields=('post_title','post_content')
	def clean_post_title(self):
		cleaned_post_title = self.cleaned_data['post_title']
		if len(cleaned_post_title.strip())!=0:
			return cleaned_post_title
                raise forms.ValidationError("Please give a title for your blog")
	def clean_post_content(self):
		cleaned_post_content = self.cleaned_data['post_content']
		if len(cleaned_post_content.strip())!=0:
			return cleaned_post_content
                raise forms.ValidationError("Blog has to have some content")
