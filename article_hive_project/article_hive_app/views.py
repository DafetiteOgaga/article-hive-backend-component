from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.html import escape
from .mock_data import *
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
# from .models import Article, Comment, Contact

# to-do (add login required decorator):
# 1. templates for members to create and post articles,
# 2. separete register to basic requirements and create
# another template to update profile info
# 3. LoginView                      ✅
# 4. LogoutView                     ✅
# 5. PasswordChangeView
# 6. PasswordResetView
# 7. PasswordResetConfirmView
# 8. PasswordResetCompleteView

# Create your views here.
def home(request):
    context = {
        'items': items,
        'rated': rated,
        'pgname': 'Home'
    }
    return render(request, 'index.html', context)

def hive(request):
    context = {
        'items': hives,
        'rated': rated,
        'pgname': 'Hive'
    }
    return render(request, 'hive.html', context)

def article(request):
    context = {
        'article': articles,
        'pgname': 'Article'
    }
    return render(request, 'article.html', context)

def about_page(request):
    context = {
        'about': about,
        'pgname': 'About'
    }
    return render(request, 'about.html', context)

def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'success'})
        return JsonResponse({'message': 'error'})
    context = {'contact': contact, 'pgname': 'Contact'}
    return render(request, 'contact.html', context)

def profile_page(request):
    context = {
        'profile': profile,
        'pgname': 'Profile'
    }
    return render(request, 'profile.html', context)

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        print(f'post: {request.POST}')
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(f'user is not None: {user is not None}')
                login(request, user)
                # return redirect('home')
                return redirect('test_authentication')
                # return JsonResponse({'message': 'success'})
        print(f'user is None')
        return JsonResponse({'message': 'error',})
    context = {
        'login': loginText,
        'pgname': 'Login'
    }
    print('Got here?')
    return render(request, 'login.html', context)

def logout_page(request):
    logout(request)
    return redirect('test_authentication')

def register_page(request):
    context = {
        'register': register,
        'pgname': 'Register'
    }
    return render(request, 'register.html', context)

def test_authentication(request):
    context = {
        'pgname': 'test_authentication'
    }
    return render(request, 'authentication.html', context)

def checkRequest(request):
    request_details1 = {
        'Method': request.method,
        'Headers': request.headers,
        'GET Parameters': request.GET,
        'POST Data': request.POST,
        'Body': request.body,
        'Files': request.FILES,
        'content_params': request.content_params,
        'content_type': request.content_type,
        'csrf_processing_done': request.csrf_processing_done,
        'encoding': request.encoding,
        'Cookies': request.COOKIES,
        'Path': request.path,
        'path_info': request.path_info,
        '_current_scheme_host': request._current_scheme_host,
        'scheme': request.scheme,
        'User': request.user,
        'session': request.session,
    }

    request_info1 = "<h1>Neccessary (need to know) Request Details</h1>"
    for key, value in request_details1.items():
        request_info1 += f"<h2>{escape(key)}</h2><pre>{escape(str(value))}</pre>"
    
    return HttpResponse(request_info1+'<br/><hr/><hr/><hr/><hr/><hr/><hr/><br/>')