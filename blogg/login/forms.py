from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    """
    User registration form. All fields are required.
    """
    first_name = forms.CharField(max_length=15, help_text="Firstname")
    last_name = forms.CharField(max_length=15, help_text="Lastname")
    email = forms.EmailField(help_text='Email ID')
    username = forms.CharField(help_text='Username', max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, max_length=15, help_text="Password")
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user