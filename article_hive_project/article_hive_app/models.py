from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # use settings.AUTH_USER_MODEL as User

# Create your models here.
class User(AbstractUser):
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=200, unique=True)
	phone = models.SmallIntegerField(null=True, blank=True)
	website = models.URLField(max_length=200, null=True, blank=True)
	joined_since = models.DateTimeField(auto_now_add=True)
	# number_of_articles = models.('Article', on_delete=models.CASCADE)
	# profile_picture = models.ImageField()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	def __str__(self):
		return self.username

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='images/', required=False)
    views = models.IntegerField(default=0)
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

class Comment(models.Model):
    comment = models.TextField(max_length=500)
    user = models.CharField(max_length=200)
    # the_article = models.ForeignKey('Article', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True) # last modified stamp

class Contact(models.Model):
    contact = models.TextField(max_length=500)
    name = models.CharField(max_length=200)
    # the_article = models.ForeignKey('Article', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # creation stamp