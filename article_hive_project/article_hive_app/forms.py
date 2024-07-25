from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from .models import User, Contact, Comment, Author_reply, About

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [ 'name', 'contact', ]

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = [ 'about', ]

class RegistrationForm(UserCreationForm):
# class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'middle_name', 'username', 'email', 'phone', 'password', 'website')
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'phone', 'password1', 'password2', 'website', 'profile_picture')
    profile_picture = forms.ImageField(required=False)

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'aboutme', 'website', 'profile_picture')
    profile_picture = forms.ImageField(required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'name']

class Author_replyForm(forms.ModelForm):
    class Meta:
        model = Author_reply
        fields = [ 'reply', ]

from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # 'author', 'date_published', 'views', and 'rating'
        fields = ['title', 'content']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Old password',
                'id': 'id_old_password',
                'type': "password",
                'class': "input-field",
                }
            )
        )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password',
                'id': 'id_new_password1',
                'type': "password",
                'class': "input-field",
                }
            )
        )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm new password',
                'id': 'id_new_password2',
                'type': "password",
                'class': "input-field",
                }
            )
        )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                }
            )
        )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password',
                'id': 'id_new_password1',
                'type': "password",
                'class': "input-field",
                }
            )
        )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm new password',
                'id': 'id_new_password2',
                'type': "password",
                'class': "input-field",
                }
            )
        )
