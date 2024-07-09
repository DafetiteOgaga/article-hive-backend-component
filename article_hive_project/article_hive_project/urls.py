"""
URL configuration for article_hive_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# from .project_views import custom_error_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('article_hive_app.urls')),     # For article_hive_app configuration.
    # path("member/", include("django.contrib.auth.urls")), # for auth
]

# handler400 = lambda request, exception: custom_error_view(request, exception, 400)
# handler401 = lambda request, exception: custom_error_view(request, exception, 401)
# handler403 = lambda request, exception: custom_error_view(request, exception, 403)
# handler404 = lambda request, exception: custom_error_view(request, exception, 404)
# handler500 = lambda request: custom_error_view(request, status_code=500)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
