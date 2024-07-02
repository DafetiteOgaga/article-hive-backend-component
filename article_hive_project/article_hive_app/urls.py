from django.urls import path
from . import views

urlpatterns = [
	# Create your urlpatterns here.
	path('ports/', views.checkRequest, name='checkRequest'),
	path('', views.home, name='home'),
]
