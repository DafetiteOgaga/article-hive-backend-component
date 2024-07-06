from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Contact, Comment

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [ 'name', 'contact', ]

class RegistrationForm(UserCreationForm):
# class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'middle_name', 'username', 'email', 'phone', 'password', 'website')
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'phone', 'password1', 'password2', 'website')

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'aboutme', 'website')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'name']

from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # 'author', 'date_published', 'views', and 'rating'
        fields = ['title', 'content']
