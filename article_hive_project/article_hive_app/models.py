from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # use settings.AUTH_USER_MODEL as User
import os, uuid, io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from PIL import Image

def unique_profile_pic(instance, filename):
	base, ext = os.path.splitext(filename)
	unique_id = uuid.uuid4().hex
	new_filename = f"{base}_{unique_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}{ext}"
	return os.path.join('profile_pictures', new_filename)

# Create your models here.
class User(AbstractUser):
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=200, unique=True)
	username = models.CharField(default="ArticleHiveUser", max_length=15)
	# username = None
	phone = models.CharField(null=True, blank=True, max_length=14)
	website = models.URLField(max_length=200, null=True, blank=True)
	profile_picture = models.ImageField(upload_to=unique_profile_pic, null=True, blank=True, default='profile_pictures/placeholder.png')
	# number_of_articles = models.ForeignKey(null=True, blank=True,)
	# rating = models.ForeignKey(null=True, blank=True)
	aboutme = models.TextField()
	# profile_picture = None

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	def __str__(self):
		return self.email

	def save(self, *args, **kwargs):
		print('entering save method ###### 1')
		print(f'isinstance(self.profile_picture, InMemoryUploadedFile: {isinstance(self.profile_picture, InMemoryUploadedFile)}')
		if (self.profile_picture or isinstance(self.profile_picture, InMemoryUploadedFile)) and self.first_name:
			img = Image.open(self.profile_picture)
			if img.mode != 'RGB':
				img = img.convert('RGB')
			min_dim = min(img.width, img.height)
			left = (img.width - min_dim) / 2
			top = (img.height - min_dim) / 2
			right = (img.width + min_dim) / 2
			bottom = (img.height + min_dim) / 2
			img = img.crop((left, top, right, bottom))
			target_size = (200, 200)
			img = img.resize(target_size, Image.LANCZOS)
			output = io.BytesIO()
			img.save(output, format='JPEG', quality=500)
			output.seek(0)
			self.profile_picture = InMemoryUploadedFile(
				output, 'ImageField', 
				f"{unique_profile_pic(self, self.profile_picture.name)}",
				'image/jpeg', 
				output.getbuffer().nbytes, 
				None
			)

		super().save(*args, **kwargs)

class Article(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
	content = models.TextField()
	date_published = models.DateTimeField(auto_now_add=True)
	# image = models.ImageField(upload_to='images/', required=False)
	views = models.IntegerField(default=0)
	# comments = models.ForeignKey('Comment', on_delete=models.CASCADE)
	rating = models.IntegerField(default=0)

	def __str__(self) -> str:
		return self.title

class Comment(models.Model):
	comment = models.TextField(max_length=500)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
	date_commented = models.DateTimeField(auto_now=True) # last modified stamp
	def __str__(self) -> str:
		return self.comment

class Author_reply(models.Model):
    reply = models.TextField(max_length=500)
    # comment = models.TextField(max_length=500)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.OneToOneField('Comment', on_delete=models.CASCADE, related_name='author_reply')
    date_replied = models.DateTimeField(auto_now=True) # last modified stamp

class Contact(models.Model):
	contact = models.TextField(max_length=500)
	name = models.CharField(max_length=200)
	# the_article = models.ForeignKey('Article', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True) # creation stamp

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.query}"

class About(models.Model):
    about = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)
