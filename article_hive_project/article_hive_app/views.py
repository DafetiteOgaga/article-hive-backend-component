from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, JsonResponse

from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode #, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required #, permission_required

from django.db.models import Q

import os #, time, requests, random, json, sys

from django.urls import reverse, reverse_lazy

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()

from .forms import RegistrationForm, ProfileUpdateForm
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm
from .forms import CustomSetPasswordForm, Author_replyForm
from .forms import ArticleForm, CommentForm, ContactForm, AboutForm

from .models import Article, Comment, Contact, Author_reply, SearchHistory
from .models import About

from .mock_data import *

from .send_mail import *

# Create your views here.
def home(request):
    articles = Article.objects.all()
    ratings = articles[::-1]
    articles = articles.order_by("?")[:8]
    context = {
        'articles': articles,
        'ratings': ratings,
        'rated': rated,
        'pgname': 'The-Article-Hive'
    }
    return render(request, 'index.html', context)

def hive(request):
    articles = Article.objects.all()
    ratings = articles[::-1]
    articles = articles.order_by("?")[:12]

    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    try:
        articles_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        articles_paginated = paginator.page(1)
    except EmptyPage:
        articles_paginated = paginator.page(paginator.num_pages)

    context = {
        'articles': articles_paginated,
        'ratings': ratings,
        'rated': rated,
        'pgname': 'Hive'
    }
    return render(request, 'hive.html', context)

def about_page(request):
    about = About.objects.all().last()
    context = {
        'about': about.about,
        'pgname': 'About'
    }
    return render(request, 'about.html', context)

@login_required
def about_form_page(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    if request.method == 'POST':
        form = AboutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('about')
    about = About.objects.all().last()
    form = AboutForm()
    context = {
        'form': form,
        'about': about.about,
    }
    return render(request, 'about_form.html', context)

def article(request, pk):
    article = Article.objects.prefetch_related('comments').filter(pk=pk).first()
    author = article.author
    article_comments = article.comments.all()

    user = request.user
    is_owner = author == user
    is_member = False
    for comment in article_comments:
        if comment.user != None and comment.user.is_active:
            is_member = True
            # print(f"Commentor {comment.user.first_name} is an active member.")
    if request.method == 'POST':
        post_data = request.POST.copy()
        if 'name' not in (dict(post_data)).keys() or post_data['name'] == '':
            post_data['name'] = 'Anonymous User'
            # request.POST.set('name', 'Anonymous User')
        form = CommentForm(post_data)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            if user.is_authenticated:
                # print(f"commentor is member: {user.first_name}")
                comment.user = request.user
            comment.save()
            # print(f"comment saved")
            if comment.user != None:
                comment_author = comment.user.first_name
            else:
                comment_author = post_data["name"]
            article_path = reverse('article', args=[pk])
            article_url = f"{request.scheme}://{request.get_host()}{article_path}"
            new_comment = article.comments.filter(comment=post_data['comment']).last()
            if new_comment == None:
                print('got from db hit the comments:', new_comment)
                new_comment = Article.objects.get(pk=pk).comments.last()
            print('the comments:', new_comment)
            response = comment_notification_email(request=request, comment_author=comment_author, comment=new_comment, article_url=article_url)
            if response.status_code == 201:
                print(f'Email sent successfully to {comment.article.author.email} # for comment')
            else:
                print(f'Failed to send email: {response.status_code}')
                print(response.text)
            return redirect('article', pk=pk)
    is_owner = author == user
    # print('is_owner:', is_owner)
    context = {
        'article': article,
        'is_owner': is_owner,
        'is_member': is_member,
        'article_comments': article_comments,
        'article_title': articles,
        'pgname': 'Article'
    }
    return render(request, 'article.html', context)

def member_hive(request, pk):
    member = User.objects.prefetch_related('articles').filter(pk=pk).first()
    # member = get_object_or_404(User, pk=pk)
    user_articles = member.articles.all()
    
    articles = Article.objects.all()
    ratings = articles[::-1]

    paginator = Paginator(user_articles, 8)
    page_number = request.GET.get('page')
    try:
        articles_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        articles_paginated = paginator.page(1)
    except EmptyPage:
        articles_paginated = paginator.page(paginator.num_pages)

    is_owner = member == request.user
    # print('is_owner:', is_owner)
    context = {
        'member': member,
        'articles': articles_paginated,
        'ratings': ratings,
        'is_owner': is_owner,
        'pgname': f"{member.first_name}'s Articles"
    }
    return render(request, 'member_hive.html', context)

@login_required
def author_response(request, pk):
    if request.method == 'POST':
        form = Author_replyForm(request.POST)
        # print('comment pk:', pk)
        comment = Comment.objects.get(pk=pk)
        pk = comment.article.pk

        # new_reply = Author_reply.objects.get(reply=form.cleaned_data['reply'])
        # print(f'new reply: {new_reply}')

        # pk = the_article.pk
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.save()
            if comment.user != None:
                # new_reply = Author_reply.objects.get(reply=form.cleaned_data['reply'])
                new_reply = comment.author_reply
                # print(f'new reply comment model: {new_reply}')
                article_path = reverse('article', args=[new_reply.comment.article.id])
                article_url = f"{request.scheme}://{request.get_host()}{article_path}"
                response = author_reply_notification_email(request=request, reply=new_reply, article_url=article_url)
                if response.status_code == 201:
                    print(f'Email sent successfully to {new_reply.comment.user.email} # for author reply')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
            return redirect('article', pk=pk)
        #     return JsonResponse({'message': 'success'})
        return JsonResponse({'message': 'error'})
    response_form = Author_replyForm()
    context = {'response_form': response_form, 'pgname': 'Author Response'}
    return render(request, 'author_comment_response_form.html', context)

def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'success'})
        return JsonResponse({'message': 'error'})
    context = {'contact': contact, 'pgname': 'Contact'}
    return render(request, 'contact.html', context)

def profile_page(request, pk):
    member = User.objects.prefetch_related('articles').filter(pk=pk).first()
    number_of_articles = member.articles.all().count()
    is_owner = member == request.user
    context = {
        'member': member,
        'is_owner': is_owner,
        'profile': profile,
        'pgname': 'Profile'
    }
    return render(request, 'profile.html', context)

@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    # print(f"User ID profile update: {user.pk}")
    old_picture = user.profile_picture
    # print(f"Old profile picture path #####: {old_picture}")
    
    if request.user != user:
        return redirect('home')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'profile_picture' in form.changed_data:
                if old_picture and old_picture.name != 'profile_pictures/placeholder.png':
                    if os.path.isfile(old_picture.path):
                        os.remove(old_picture.path)
                new_picture = form.cleaned_data['profile_picture']
                # Check if the new picture is an uploaded file
                if isinstance(new_picture, InMemoryUploadedFile):
                    user.profile_picture = new_picture
            user.save()
            return redirect('profile', pk=pk)
        return JsonResponse({'message': 'form invalid', 'errors': form.errors})
    form = ProfileUpdateForm(instance=user)
    context = {
        'profile': user,
        'form': form,
        'updateprofile': updateprofile,
        'pgname': 'Update-profile'
    }
    return render(request, 'profile_update.html', context)


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # print(f'user is not None: {user is not None}')
                login(request, user)
                return redirect('home')
            return JsonResponse({'message': 'not registered',})
        return JsonResponse({'message': 'error',})
    context = {
        'login': loginText,
        'pgname': 'Login'
    }
    return render(request, 'login.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # print(f'form.is_valid: {form.is_valid()}')
            user = form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1') # mandatory
            if request.POST.get('password1') == request.POST.get('password2'):
                user = authenticate(username=username, password=password)
                login(request, user)
                article_url = f"{request.scheme}://{request.get_host()}"
                response = welcome_email(request=request, user=user, article_url=article_url)
                if response.status_code == 201:
                    print(f'Email sent successfully to {user.email} # for registration')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
                return redirect('home')
            return JsonResponse({'message': 'incorrect password'})
        return JsonResponse({'message': 'form invalid', 'errors': form.errors})
    context = {
        'register': register,
        'pgname': 'Register'
    }
    return render(request, 'register.html', context)

@login_required
def article_form(request):
    pk=request.user.id
    # print('user id:', pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            user = User.objects.prefetch_related('articles').filter(pk=pk).first()
            if user.articles.all().count() == 1:
                article_path = reverse('article_form')
                article_url = f"{request.scheme}://{request.get_host()}{article_path}"
                response = congratulations_first_post(request=request, user=user, article_url=article_url)
                if response.status_code == 201:
                    print(f'Email sent successfully to {user.email} # for first post')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
            return redirect('member_hive', pk=pk)
    form = ArticleForm()
    context = {
        'form': form,
        'article': 'Post an Article',
        'pgname': 'Post an Article'
    }
    return render(request, 'article_form.html', context)

@login_required
def update_article_form(request, pk):
    article = get_object_or_404(Article, pk=pk)
    author = article.author
    if request.user != author:
        return redirect('home')
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            article.author = request.user
            article.save()
            return redirect('article', pk=pk)
    context = {
        'article': article,
        'article_title': 'Update Article',
        'pgname': 'Update Article'
    }
    return render(request, 'update_article_form.html', context)

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'auth/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        email_response = password_change_done_email(request=self.request, user=user) #, article_url=article_url)
        if email_response.status_code == 201:
            print(f'Email sent successfully to {user.email} # for password change done')
        else:
            print(f'Failed to send email: {email_response.status_code}')
            print(email_response.text)
        return response

    def form_invalid(self, form):
        return JsonResponse({'message': 'form invalid', 'errors': form.errors}, status=400)

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'

def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            # print(f"get user: {user}")
            if user:
                protocol = request.scheme
                domain = request.get_host()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                # required
                reset_link = f"{protocol}://{domain}{reset_url}"
                response = send_password_reset_email(request=request, user=user, reset_link=reset_link)
                if response.status_code == 201:
                    print(f'Email sent successfully to {user.email} # for password reset sent')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
                    return redirect('oopsy')
            else:
                return redirect('password_reset_failed')
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'auth/password_reset_form.html', {'form': form})

def password_reset_failed_view(request):
    return render(request, 'auth/password_reset_failed.html')

def oopsy_view(request):
    return render(request, 'auth/oopsy.html')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'auth/password_reset_confirm_form.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_invalid(self, form):
        return JsonResponse({'message': 'form invalid', 'errors': form.errors}, status=400)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.user
        try:
            email_response = password_reset_complete_email(request=self.request, user=user) #, article_url=article_url)
            if email_response.status_code == 201:
                print(f'Email sent successfully to {user.email} # for password reset complete')
            else:
                print(f'Failed to send email: {email_response.status_code}')
                print(email_response.text)
        except Exception as e:
            print(f"Error during sending password change email: {str(e)}")
        return response

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'

def is_superuser(req_obj):
    if req_obj.user.is_authenticated and req_obj.user.is_superuser:
        return True
    return False

def feedback_contact_list_view(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedbacks = Contact.objects.all().order_by('-id')
    print(f"feedbacks:", feedbacks)
    paginator = Paginator(feedbacks, 8)
    page_number = request.GET.get('page')
    print(f"page_number:", page_number)
    try:
        feedbacks_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        feedbacks_paginated = paginator.page(1)
    except EmptyPage:
        feedbacks_paginated = paginator.page(paginator.num_pages)
    context = {
        'feedbacks': feedbacks_paginated,
        'pgname': 'Feedback'
    }
    return render(request, 'admin_plates/feedback_contact_list_view.html', context)

def feedback_contact_detail_view(request, pk):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(Contact, pk=pk)
    context = {
        'feedback': feedback,
        'pgname': 'Feedback Details'
    }
    return render(request, 'admin_plates/feedback_contact_detail_view.html', context)

def feedback_member_hive_view(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedbacks = Article.objects.all().order_by('-id')
    paginator = Paginator(feedbacks, 8)
    page_number = request.GET.get('page')
    try:
        feedbacks_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        feedbacks_paginated = paginator.page(1)
    except EmptyPage:
        feedbacks_paginated = paginator.page(paginator.num_pages)
    context = {
        'feedbacks': feedbacks_paginated,
        'ratings': feedbacks,
        'pgname': 'Feedback'
    }
    return render(request, 'admin_plates/feedback_member_hive_view.html', context)

def feedback_member_detail_view(request, pk):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedback = Article.objects.prefetch_related('comments').filter(pk=pk).first()
    author = feedback.author
    article_comments = feedback.comments.all()

    user = request.user
    is_owner = author == user
    is_member = False
    for comment in article_comments:
        if comment.user != None and comment.user.is_active:
            is_member = True
            print(f"Commentor {comment.user.first_name} is an active member.")
    is_owner = author == user
    # print('is_owner:', is_owner)
    context = {
        'feedback': feedback,
        'article_comments': article_comments,
        'pgname': 'Feedback Details'
    }
    return render(request, 'admin_plates/feedback_member_detail_view.html', context)

def feedback_author_reply_list_view(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedbacks = Author_reply.objects.all().order_by('-id')
    paginator = Paginator(feedbacks, 8)
    page_number = request.GET.get('page')
    try:
        feedbacks_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        feedbacks_paginated = paginator.page(1)
    except EmptyPage:
        feedbacks_paginated = paginator.page(paginator.num_pages)
    context = {
        'feedbacks': feedbacks_paginated,
        'pgname': 'Feedback'
    }
    return render(request, 'admin_plates/feedback_author_reply_list_view.html', context)

def feedback_author_reply_detail_view(request, pk):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(Author_reply, pk=pk)
    context = {
        'feedback': feedback,
        'pgname': 'Feedback Details'
    }
    return render(request, 'admin_plates/feedback_author_reply_detail_view.html', context)



def feedback_comment_list_view(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedbacks = Comment.objects.all().order_by('-id')
    paginator = Paginator(feedbacks, 8)
    page_number = request.GET.get('page')
    try:
        feedbacks_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        feedbacks_paginated = paginator.page(1)
    except EmptyPage:
        feedbacks_paginated = paginator.page(paginator.num_pages)
    context = {
        'feedbacks': feedbacks_paginated,
        'pgname': 'Feedback'
    }
    return render(request, 'admin_plates/feedback_comment_list_view.html', context)

def feedback_comment_detail_view(request, pk):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(Comment, pk=pk)
    context = {
        'feedback': feedback,
        'pgname': 'Feedback Details'
    }
    return render(request, 'admin_plates/feedback_comment_detail_view.html', context)

def feedback_user_list_view(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedbacks = User.objects.all().order_by('-id')
    paginator = Paginator(feedbacks, 8)
    page_number = request.GET.get('page')
    try:
        feedbacks_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        feedbacks_paginated = paginator.page(1)
    except EmptyPage:
        feedbacks_paginated = paginator.page(paginator.num_pages)
    context = {
        'feedbacks': feedbacks_paginated,
        'pgname': 'Feedback'
    }
    return render(request, 'admin_plates/feedback_user_list_view.html', context)

def feedback_user_detail_view(request, pk):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(User, pk=pk)
    _is_active = feedback.is_active
    _is_staff = feedback.is_staff
    _is_superuser = feedback.is_superuser
    _profile_picture = feedback.profile_picture.url
    context = {
        'feedback': feedback,
        'is_active': _is_active,
        'is_staff': _is_staff,
        'is_superuser': _is_superuser,
        'profile_picture': _profile_picture,
        'pgname': 'Feedback Details'
    }
    return render(request, 'admin_plates/feedback_user_detail_view.html', context)

def feedback_search_history_list_view(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedbacks = SearchHistory.objects.all().order_by('-id')
    paginator = Paginator(feedbacks, 8)
    page_number = request.GET.get('page')
    try:
        feedbacks_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        feedbacks_paginated = paginator.page(1)
    except EmptyPage:
        feedbacks_paginated = paginator.page(paginator.num_pages)
    context = {
        'feedbacks': feedbacks_paginated,
        'pgname': 'Feedback'
    }
    return render(request, 'admin_plates/feedback_search_history_list_view.html', context)

def feedback_list_view(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    context = {
        'feedbacks': [
            {'title': 'Articles', 'url': 'article/'},
            {'title': 'Author Replies', 'url': 'author-reply/'},
            {'title': 'Comments', 'url': 'comment/'},
            {'title': 'Contacts', 'url': 'contact/'},
            {'title': 'Users', 'url': 'user/'},
            {'title': 'SearchHistory', 'url': 'search-history/'},
        ],
        'pgname': 'Feedback Details'
    }
    return render(request, 'admin_plates/feedback_list_view.html', context)

def advanced_search(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    if query:
        # User
        user_results = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(aboutme__icontains=query)
        )

        # Article
        article_results = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

        # Comment
        comment_results = Comment.objects.filter(
            Q(comment__icontains=query) |
            Q(name__icontains=query)
        )

        # Author_reply
        reply_results = Author_reply.objects.filter(
            Q(reply__icontains=query)
        )

        # Contact
        contact_results = Contact.objects.filter(
            Q(contact__icontains=query) |
            Q(name__icontains=query)
        )

        # Combine all results
        all_results = list(user_results) + list(article_results) + list(comment_results) + list(reply_results) + list(contact_results)
        
        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=query)
    else:
        all_results = []
    
    paginator = Paginator(all_results, 10)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    
    history = []
    if request.user.is_authenticated:
        history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
    
    context = {
        'results': results,
        'query': query,
        'history': history,
    }
    
    return render(request, 'partials/_search_results.html', context)

def autocomplete(request):
    query = request.GET.get('q', '')
    
    # Autocomplete for Article titles
    article_results = Article.objects.filter(title__istartswith=query)[:3]
    
    # Autocomplete for User names
    user_results = User.objects.filter(
        Q(username__istartswith=query) |
        Q(first_name__istartswith=query) |
        Q(last_name__istartswith=query)
    )[:2]
    
    data = (
        list(article_results.values('id', 'title')) +
        list(user_results.values('id', 'username', 'first_name', 'last_name'))
    )
    
    return JsonResponse(data, safe=False)

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

def test_email_view(request):
    try:
        send_mail(
            'Test Email Subject',
            'This is a test email body.',
            'ogagadafetite@gmail.com',
            ['bettydafetiteogaga@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')