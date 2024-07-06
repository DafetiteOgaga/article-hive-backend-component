from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # use settings.AUTH_USER_MODEL as User

# Create your models here.
class User(AbstractUser):
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=200, unique=True)
	username = None
	phone = models.CharField(null=True, blank=True, max_length=14)
	website = models.URLField(max_length=200, null=True, blank=True)
	# profile_picture = models.ImageField()
	# number_of_articles = models.ForeignKey(null=True, blank=True,)
	# rating = models.ForeignKey(null=True, blank=True)
	aboutme = models.TextField()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	def __str__(self):
		return self.email

class Article(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
	content = models.TextField()
	date_published = models.DateTimeField(auto_now_add=True)
	# image = models.ImageField(upload_to='images/', required=False)
	views = models.IntegerField(default=0)
	# comments = models.ForeignKey('Comment', on_delete=models.CASCADE)
	rating = models.IntegerField(default=0)

class Comment(models.Model):
	comment = models.TextField(max_length=500)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
	date_commented = models.DateTimeField(auto_now=True) # last modified stamp

class Contact(models.Model):
	contact = models.TextField(max_length=500)
	name = models.CharField(max_length=200)
	# the_article = models.ForeignKey('Article', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True) # creation stamp