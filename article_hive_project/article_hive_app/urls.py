from django.urls import path
from . import views

urlpatterns = [
	# Create your urlpatterns here.
	path('', views.home, name='home'),


	path('ports/', views.checkRequest, name='checkRequest'),
]
