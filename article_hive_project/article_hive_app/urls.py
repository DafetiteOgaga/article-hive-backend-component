from django.urls import path
from . import views

urlpatterns = [
	# Create your urlpatterns here.
	path('', views.home, name='home'),
	path('hive/', views.hive, name='hive'),
	path('article/', views.article, name='article'),
	path('about/', views.about_page, name='about'),
	path('contact/', views.contact_page, name='contact'),
	path('profile/', views.profile_page, name='profile'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),
	path('register/', views.register_page, name='register'),



	path('test_authentication/', views.test_authentication, name='test_authentication'),
	path('ports/', views.checkRequest, name='checkRequest'),
]
