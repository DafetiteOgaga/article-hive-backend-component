from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.html import escape
from .mock_data import *
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ContactForm, RegistrationForm, ProfileUpdateForm, ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

# from .models import Article, Comment, Contact

# to-do (add login required decorator):
# 5. PasswordChangeView
# 6. PasswordResetView
# 7. PasswordResetConfirmView
# 8. PasswordResetCompleteView
#10. pagination for hive page
#11. register the models with admin

# Create your views here.
def home(request):
    articles = Article.objects.all()[:8]
    context = {
        'articles': articles,
        # 'items': items,
        'rated': rated,
        'pgname': 'Home'
    }
    return render(request, 'index.html', context)

def hive(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
        # 'items': hives,
        'rated': rated,
        'pgname': 'Hive'
    }
    return render(request, 'hive.html', context)

def article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    author = article.author
    user = request.user
    # print('author:', author)
    # print('user:', user)
    is_owner = author == user
    # print('is_owner:', is_owner)
    context = {
        'article': article,
        'is_owner': is_owner,
        'article_title': articles,
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
        print('request.Post:', request.POST)
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            form.save()
            return JsonResponse({'message': 'success'})
        return JsonResponse({'message': 'error'})
    context = {'contact': contact, 'pgname': 'Contact'}
    return render(request, 'contact.html', context)

def profile_page(request, pk):
    member = get_object_or_404(User, pk=pk)
    print(f"User ID profile: {member.pk}")
    context = {
        'member': member,
        'profile': profile,
        'pgname': 'Profile'
    }
    return render(request, 'profile.html', context)

@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    print(f"User ID profile update: {user.pk}")
    
    if request.user != user:
        return redirect('home')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        print(f'form content: {request.POST}')
        # print('###################################')
        # print(f'form: {form}')
        # print('###################################')
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            # user = form.save()
            form.save()
            # return redirect('home')
            return redirect('profile', pk=pk)
            # # password = form.get('password')
            # # password2 = form.get('password2')
            # # print(f'password (before): {password}')
            # # print(f'password2 (before): {password2}')
            # username = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1') # mandatory
            # # password2 = form.cleaned_data.get('password2')
            # # print(f'password (after): {password}')
            # # print(f'password2 (after): {password2}')
            # if request.POST.get('password1') == request.POST.get('password2'):
            #     print(f"password == password2: {request.POST.get('password') == request.POST.get('password2')}")
            #     user = authenticate(username=username, password=password)
            #     login(request, user)
            #     # return redirect('home')
            #     return redirect('test_authentication')
            # return JsonResponse({'message': 'incorrect password'})
        # print('###################################')
        # print(f'Form errors: {form.errors}')
        # print('###################################')
        return JsonResponse({'message': 'form invalid', 'errors': form.errors})
    form = ProfileUpdateForm(instance=user)
    context = {
        'profile': user,
        'form': form,
        'updateprofile': updateprofile,
        'pgname': 'Update-profile'
    }
    print(f'form: Error')
    print('###################################')
    print(f'Form errors: {form.errors}')
    print('###################################')
    return render(request, 'profile_update.html', context)


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        # print(f'post: {request.POST}')
        if form.is_valid():
            # print(f'form.is_valid: {form.is_valid()}')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # print(f'user is not None: {user is not None}')
                login(request, user)
                # return redirect('home')
                return redirect('home')
                # return JsonResponse({'message': 'success'})
        # print(f'user is None')
        return JsonResponse({'message': 'error',})
    context = {
        'login': loginText,
        'pgname': 'Login'
    }
    # print('Got here?')
    return render(request, 'login.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(f'form content: {request.POST}')
        # print('###################################')
        # print(f'form: {form}')
        # print('###################################')
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            user = form.save()
            # password = form.get('password')
            # password2 = form.get('password2')
            # print(f'password (before): {password}')
            # print(f'password2 (before): {password2}')
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1') # mandatory
            # password2 = form.cleaned_data.get('password2')
            # print(f'password (after): {password}')
            # print(f'password2 (after): {password2}')
            if request.POST.get('password1') == request.POST.get('password2'):
                print(f"password == password2: {request.POST.get('password') == request.POST.get('password2')}")
                user = authenticate(username=username, password=password)
                login(request, user)
                # return redirect('home')
                return redirect('home')
            return JsonResponse({'message': 'incorrect password'})
        print('###################################')
        print(f'Form errors: {form.errors}')
        print('###################################')
        return JsonResponse({'message': 'form invalid', 'errors': form.errors})
    context = {
        'register': register,
        'pgname': 'Register'
    }
    print(f'form: auth registration failed')
    print('###################################')
    print(f'Form errors: {form.errors}')
    print('###################################')
    return render(request, 'register.html', context)

@login_required
def article_form(request):
    # user = get_object_or_404(User, pk=pk)
    # if request.user != user:
    #     return redirect('home')
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        print(f'form content: {request.POST}')
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            # return redirect('article_detail', pk=pk)
            return redirect('hive')
    form = ArticleForm()
    context = {
        'form': form,
        'article': 'Post an Article',
        'pgname': 'Post an Article'
    }
    print(f'just an empty form')
    return render(request, 'article_form.html', context)
#########################################################################################################
# def article_list(request):
#     articles = Article.objects.all()
#     context = {
#         'articles': articles
#         }
#     return render(request, 'article_list.html', context)
#########################################################################################################
# def article_detail(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     return render(request, 'article_detail.html', {'article': article})
#########################################################################################################
#########################################################################################################
@login_required
def update_article_form(request, pk):
    article = get_object_or_404(Article, pk=pk)
    author = article.author
    print('author:', author)
    # user = get_object_or_404(User, pk=pk)
    print('request.user:', request.user)
    print('registered user:', author)
    if request.user != author:
        return redirect('home')
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        print(f'form content: {request.POST}')
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            # print(f'form: {form}')
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            # article = form.save(commit=False)
            article.author = request.user
            article.save()
            # return redirect('article_detail', pk=pk)
            return redirect('article', pk=pk)
    # field = get_object_or_404(Article, pk=pk)
    print('article:', article)
    context = {
        'article': article,
        'article_title': 'Update Article',
        'pgname': 'Update Article'
    }
    print(f'just an empty form')
    return render(request, 'update_article_form.html', context)
#########################################################################################################


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