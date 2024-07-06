from django.urls import path
from . import views

urlpatterns = [
	# Create your urlpatterns here.
	path('', views.home, name='home'),
	path('hive/', views.hive, name='hive'),
	path('article/<int:pk>/', views.article, name='article'),
	path('about/', views.about_page, name='about'),
	path('contact/', views.contact_page, name='contact'),
	path('profile/<int:pk>/', views.profile_page, name='profile'),
	path('profile-update/<int:pk>/', views.profile_update, name='profile_update'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),
	path('register/', views.register_page, name='register'),


	# path('article/new/<int:pk>/', views.article_form, name='article_form'),
	path('article/new/', views.article_form, name='article_form'),
	path('update-article-form/<int:pk>/', views.update_article_form, name='update_article_form'),


	# path('', views.article_list, name='article_list'),
    # path('article/<int:pk>/', views.article_detail, name='article_detail'),


	path('test_authentication/', views.test_authentication, name='test_authentication'),
	path('ports/', views.checkRequest, name='checkRequest'),
]
