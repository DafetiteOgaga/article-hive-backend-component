from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, JsonResponse

from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode #, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required #, permission_required

# from django.conf import settings

from django.db.models import Q

import os #, time, requests, random, json, sys

from django.urls import reverse, reverse_lazy

# from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()

from .forms import RegistrationForm, ProfileUpdateForm
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm
from .forms import CustomSetPasswordForm, Author_replyForm
from .forms import ArticleForm, CommentForm, ContactForm

from .models import Article, Comment, Contact, Author_reply, SearchHistory

from .mock_data import *

from .send_mail import *

# Create your views here.
def home(request):
    articles = Article.objects.all()
    ratings = articles[::-1]
    # ratings = articles.reverse()
    articles = articles.order_by("?")[:8]
    # articles = articles[:8]
    # random.shuffle(articles)
    context = {
        'articles': articles,
        'ratings': ratings,
        # 'items': items,
        'rated': rated,
        'pgname': 'The-Article-Hive'
    }
    return render(request, 'index.html', context)

def hive(request):
    articles = Article.objects.all()
    ratings = articles[::-1]
    # ratings = articles.reverse()
    articles = articles.order_by("?")[:8]
    # articles = list(articles)
    # random.shuffle(articles)

    paginator = Paginator(articles, 8)
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
        # 'items': hives,
        'rated': rated,
        'pgname': 'Hive'
    }
    return render(request, 'hive.html', context)

def article(request, pk):
    # article = get_object_or_404(Article, pk=pk)
    # article_comments = Comment.objects.filter(article=article).select_related('author_reply')
    # author = article.author
    
    article = Article.objects.prefetch_related('comments').filter(pk=pk).first()
    author = article.author
    article_comments = article.comments.all()
    # print(f"article2 #1 : {article2}")
    print(f"article #1 : {article}")
    print()
    # print(f"author2 #1 : {author2}")
    print(f"author #1 : {author}")
    print()
    # print(f"comments #1 : {comments2}")
    print(f"article_comments #1 : {article_comments}")
    print()

    user = request.user
    is_owner = author == user
    is_member = False
    for comment in article_comments:
        if comment.user != None and comment.user.is_active:
            is_member = True
            print(f"Commentor {comment.user.first_name} is an active member.")
        else:
            print(f"Commentor is not an active member.")
    # is_member = article_comments.user.is_active()
    if request.method == 'POST':
        print(f'original request payload: {request.POST}')
        post_data = request.POST.copy()
        print(f'copied request payload: {post_data}')
        print(f'copied request payload dict: {dict(post_data)}')
        print(f'copied request payload dict-keys: {(dict(post_data).keys())}')
        if 'name' not in (dict(post_data)).keys() or post_data['name'] == '':
            post_data['name'] = 'Anonymous User'
            # request.POST.set('name', 'Anonymous User')
        form = CommentForm(post_data)
        if form.is_valid():
            print(f'form is valid: {form.is_valid()}')
            comment = form.save(commit=False)
            comment.article = article
            # if is_owner:
            #     print(f"commentor is author: {author.first_name}")
            #     comment.user = 'Author'
            if user.is_authenticated:
                print(f"commentor is member: {user.first_name}")
                comment.user = request.user
            else:
                print(f"commentor is guest: Guest")
                # comment.user = 'Anonymous Reader'
            comment.save()
            print(f"comment saved")
            if comment.user != None:
                comment_author = comment.user.first_name
            else:
                comment_author = post_data["name"]
            article_path = reverse('article', args=[pk])
            article_url = f"{request.scheme}://{request.get_host()}{article_path}"
            new_comment = Comment.objects.get(comment=post_data['comment'])
            print(f"article: {article}")
            print(f"comment_author: {comment_author}")
            print(f"new_comment: {new_comment}")
            response = comment_notification_email(request=request, comment_author=comment_author, comment=new_comment, article_url=article_url)
            # sys.exit(0)
            if response.status_code == 201:
                    print(f'Email sent successfully to {comment.article.author.email}')
            else:
                print(f'Failed to send email: {response.status_code}')
                print(response.text)
            return redirect('article', pk=pk)
    # article = get_object_or_404(Article, pk=pk)
    # author = article.author
    # user = request.user
    # print('author:', author)
    # print('user:', user)
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

def article_list(request, pk):
    member = User.objects.prefetch_related('articles').filter(pk=pk).first()
    # member = get_object_or_404(User, pk=pk)
    user_articles = member.articles.all()
    
    articles = Article.objects.all()
    ratings = articles[::-1]
    # ratings = articles.reverse()
    print(f'pk #1: {pk}')
    print(f'member #1: {member}')
    # print(f'member #2: {article1}')
    print()
    print(f'user_articles #1: {user_articles}')
    # print(f'user_articles #2: {article1.articles.all()}')
    print()
    # print(f'user_articles #1: {user_articles}')
    # print(f'user_articles #2: {article1.user.all()}')
    print()
    

    paginator = Paginator(user_articles, 8)
    page_number = request.GET.get('page')
    try:
        articles_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        articles_paginated = paginator.page(1)
    except EmptyPage:
        articles_paginated = paginator.page(paginator.num_pages)

    # author = article.author
    # user = request.user
    # print('author:', author)
    # print('user:', user)
    is_owner = member == request.user
    # print('is_owner:', is_owner)
    context = {
        'member': member,
        'articles': articles_paginated,
        'ratings': ratings,
        'is_owner': is_owner,
        # 'article_title': articles,
        'pgname': f"{member.first_name}'s Articles"
    }
    return render(request, 'article_list.html', context)

@login_required
def author_response(request, pk):
    if request.method == 'POST':
        form = Author_replyForm(request.POST)
        print('comment pk:', pk)
        comment = Comment.objects.get(pk=pk)
        print('comment:', comment)
        the_article = comment.article
        print('the_article:', the_article)
        pk = the_article.pk
        print('article pk:', pk)
        print('request.Post:', request.POST)
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            reply = form.save(commit=False)
            reply.comment = comment
            reply.save()
            print(f"response saved")
            # protocol = request.scheme
            # domain = request.get_host()
            if comment.user != None:
                new_reply = Author_reply.objects.get(reply=form.cleaned_data['reply'])
                article_path = reverse('article', args=[new_reply.comment.article.id])
                article_url = f"{request.scheme}://{request.get_host()}{article_path}"
                response = author_reply_notification_email(request=request, reply=new_reply, article_url=article_url)
                if response.status_code == 201:
                        print(f'Email sent successfully to {new_reply.comment.user.email}')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
            return redirect('article', pk=pk)
        #     return JsonResponse({'message': 'success'})
        return JsonResponse({'message': 'error'})
    response_form = Author_replyForm()
    context = {'response_form': response_form, 'pgname': 'Author Response'}
    return render(request, 'author_comment_response_form.html', context)


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
    member = User.objects.prefetch_related('articles').filter(pk=pk).first()
    # member = get_object_or_404(User, pk=pk)
    print(f"User ID profile: {member.pk}")
    print(f"Profile picture path: {member.profile_picture}")
    print(f"Profile aboutme path: {member.aboutme}")
    print(f"member #1: {member}")
    # print(f"prof #2: {prof}")
    
    # number_of_articles = member.articles.all().count()
    # print(f"Number of articles #1: {number_of_articles}")
    number_of_articles = member.articles.all().count()
    print(f"Number of articles #2: {number_of_articles}")
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
    print(f"User ID profile update: {user.pk}")
    old_picture = user.profile_picture
    print(f"Old profile picture path #####: {old_picture}")
    
    if request.user != user:
        return redirect('home')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        print(f'form content: {request.POST}')
        # print('###################################')
        # print(f'form: {form}')
        # print('###################################')
        if form.is_valid():
            print(f'form.is_valid: {form.is_valid()}')
            print(f'form cleaned data: {form.cleaned_data}')
            print(f'form changed data: {form.changed_data}')
            print(f'str(user.profile_picture) ### 1 : {str(user.profile_picture)}')
            if 'profile_picture' in form.changed_data:
                if old_picture and old_picture.name != 'profile_pictures/placeholder.png':
                    if os.path.isfile(old_picture.path):
                        os.remove(old_picture.path)
                # if str(old_picture) != 'profile_pictures/placeholder.png':
                #     print(f'old_picture is NOT placeholder ### 2 : {str(old_picture) == "profile_pictures/placeholder.png"}')
                #     old_picture.delete(save=False)  # Delete the old profile picture from the filesystem
                # else:
                #     print(f'old_picture is placeholder ### 2 : {str(old_picture) == "profile_pictures/placeholder.png"}')
                new_picture = form.cleaned_data['profile_picture']
                # Check if the new picture is an uploaded file
                if isinstance(new_picture, InMemoryUploadedFile):
                    user.profile_picture = new_picture
                # user.profile_picture = form.cleaned_data['profile_picture']
                # user.profile_picture = 'profile_pictures/placeholder.png'
            # user = form.save()
            # form.save()
            user.save()
            # old_picture.delete()
            # return redirect('home')
            # time.sleep(2)
            return redirect('profile', pk=pk)
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
        print(f'post: {request.POST}')
        print(f'form.is_valid: {form.is_valid()}')
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
            return JsonResponse({'message': 'not registered',})
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
        form = RegistrationForm(request.POST, request.FILES)
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
                article_url = f"{request.scheme}://{request.get_host()}"
                response = welcome_email(request=request, user=user, article_url=article_url)
                if response.status_code == 201:
                    print(f'Email sent successfully to {user.email}')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
                    # return redirect('oopsy')
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
    pk=request.user.id
    print('user id:', pk)
    # user = User.objects.prefetch_related('articles').filter(pk=pk).first()
    # print('user:', user)
    # print('all articles:', user.articles.all())
    # print('no of articles:', user.articles.all().count())
    # k =1
    # if k != 1:
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
            user = User.objects.prefetch_related('articles').filter(pk=pk).first()
            print('user:', user)
            print('all articles:', user.articles.all())
            print('no of articles:', user.articles.all().count())
            if user.articles.all().count() == 1:
                article_path = reverse('article_form')
                article_url = f"{request.scheme}://{request.get_host()}{article_path}"
                response = congratulations_first_post(request=request, user=user, article_url=article_url)
                if response.status_code == 201:
                    print(f'Email sent successfully to {user.email}')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
            return redirect('article_list', pk=pk)
    form = ArticleForm()
    context = {
        'form': form,
        'article': 'Post an Article',
        'pgname': 'Post an Article'
    }
    print(f'just an empty form')
    return render(request, 'article_form.html', context)

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

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'auth/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        print('111111111111111111')
        response = super().form_valid(form)
        print('22222222222222222222')
        user = self.request.user
        # article_path = reverse('contact')
        # article_url = f"{self.request.scheme}://{self.request.get_host()}{article_path}"
        email_response = password_change_done_email(request=self.request, user=user) #, article_url=article_url)

        # print(f"Password change form is valid. User: {user}, Article URL: {article_url}")
        if email_response.status_code == 201:
            print(f'Email sent successfully to {user.email}')
        else:
            print(f'Failed to send email: {email_response.status_code}')
            print(email_response.text)
        print('3333333333333333333333333')
        return response

    def form_invalid(self, form):
        print(f"Password change form is invalid. Errors: {form.errors}")

        print('###################################')
        print(f'Form errors: {form.errors}')
        print('###################################')

        return JsonResponse({'message': 'form invalid', 'errors': form.errors}, status=400)

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'
    # def dispatch(self, request, *args, **kwargs):
    #     user = request.user
    #     article_path = reverse('contact')
    #     article_url = f"{request.scheme}://{request.get_host()}{article_path}"
    #     response = password_change_done_email(user=user, article_url=article_url)
    #     if response.status_code == 201:
    #         print(f'Email sent successfully to {user.email}')
    #     else:
    #         print(f'Failed to send email: {response.status_code}')
    #         print(response.text)

    #     return super().dispatch(request, *args, **kwargs)

########################################################################
# from django.core.mail import EmailMessage
########################################################################
# class CustomPasswordResetView(auth_views.PasswordResetView):
#     form_class = CustomPasswordResetForm
#     template_name = 'auth/password_reset_form.html'
#     # for backend email
#     email_template_name = 'auth/password_reset_email.html'
#     subject_template_name = 'auth/password_reset_subject.txt'
#     success_url = '/password_reset/done/'

#     # ........................................................................

#     def form_valid(self, form):
#         response = super().form_valid(form)  # Call the original form_valid method

#         # Iterate through users and send password reset email via FastAPI
#         user = get_object_or_404(User, email=form.cleaned_data['email'])
#         if user:
#             protocol = self.request.scheme
#             domain = self.request.get_host()
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)
#             reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
#             # required
#             reset_link = f"{protocol}://{domain}{reset_url}"
#             url = 'https://api.brevo.com/v3/smtp/email'
#             subjectx = self.subject_template_name, {'user': user}

#             email_data = {
#                 'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
#                 'to': [{'email': f'{user}', 'name': f'{user.first_name}'}],
#                 'subject': f'{render_to_string(subjectx.strip())}',
#                 'htmlContent': f'<html><body><h1>This is a test email</h1><p>{reset_link}</p><p>Hello, this is a test email sent using Brevo API.</p></body></html>',
#                 'textContent': 'This is a textContent test email. Hello, this the textContent test email sent using Brevo API.'
#             }
#             headers = {
#                 'accept': 'application/json',
#                 'api-key': api_key,
#                 'content-type': 'application/json'
#             }
#             response = requests.post(url, headers=headers, data=json.dumps(email_data))
#             if response.status_code == 201:
#                 print('Email sent successfully')
#             else:
#                 print(f'Failed to send email: {response.status_code}')
#                 print(response.text)

            
#             # Render the email body and subject templates
#             email_body = render_to_string(self.email_template_name, {
#                 'user': user,
#                 'protocol': protocol,
#                 'domain': domain,
#                 'uid': uid,
#                 'token': token,
#                 'reset_link': reset_link
#             })
#             email_subject = render_to_string(self.subject_template_name, {'user': user}).strip()
#             print('######################################################################')
#             print(f'email_subject: {email_subject}')
#             print('######################################################################')
#             print(f'email_body: {email_body}')
#             print('######################################################################')

#             # # Prepare email data to be sent to FastAPI
#             # email_data = {
#             #     "email": user.email,
#             #     "subject": email_subject,
#             #     "body": email_body
#             # }
#             # send_email = EmailMessage(
#             #     subject=email_data['subject'],
#             #     body=email_data['body'],
#             #     from_email="ogagadafetite@gmail.com",
#             #     to=[email_data['email']]
#             # )
#             # send_email.send()
#             # print(f'email_data: {email_data}')
#             # print('######################################################################')
#             # print('####################### EMAIL SENT! #################################')
#             # print('######################################################################')

#             # # # Send a POST request to FastAPI email sending endpoint
#             # # requests.post("http://localhost:8000/send-email/", json=email_data)
#             # print(f'RESPONSE: {response} #####################')
#             # print('######################################################################')
#         return response  # Return the original response
    

def custom_password_reset(request):
    print('in password reset logic')
    # print(f"my key #0: {api_key}")
    print(f"request.method: {request.method}")
    if request.method == 'POST':
        print(f"request.POST: {request.POST}")
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            print(f"form.is_valid: {form.is_valid()}")
            email = form.cleaned_data['email']
            print(f"email: {email}")
            # user = get_object_or_404(User, email=email)
            user = User.objects.filter(email=email).first()
            print(f"get user: {user}")
            if user:
                # user.first()
                print(f"if user: {user != None}")
                protocol = request.scheme
                domain = request.get_host()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                # required
                reset_link = f"{protocol}://{domain}{reset_url}"
                # url = 'https://api.brevo.com/v3/smtp/email'

                # Render the subject template
                # subject = render_to_string('auth/password_reset_subject.txt', {'user': user}).strip()
                # email_body = render_to_string('auth/password_reset_email.html', {
                #     'user': user.first_name,
                #     'reset_link': reset_link
                # })

                # print(f"my key #1: {api_key}")
                # print(f"user: {user}")
                # print(f"email: {user.email}")
                # print(f"firstname: {user.first_name}")
                # print(f"subject: {subject}")
                # print(f"reset link: {reset_link}")
                # Email data to be sent to Brevo
                # email_data = {
                #     'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},  # Sender info
                #     'to': [{'email': user.email, 'name': user.first_name}],  # Recipient info
                #     'subject': subject,  # Subject line
                #     'htmlContent': f'{email_body}',  # HTML content
                #     'textContent': f'Password Reset Link: {reset_link}'  # Text content
                # }

                # # Request headers
                # headers = {
                #     'accept': 'application/json',  # Accept JSON response
                #     'api-key': api_key,  # API key header
                #     'content-type': 'application/json'  # Content type header
                # }

                # Send POST request to Brevo
                # response = requests.post(url, headers=headers, data=json.dumps(email_data))
                response = send_password_reset_email(request=request, user=user, reset_link=reset_link)
                if response.status_code == 201:  # Check if email was sent successfully
                    print(f'Email sent successfully to {user.email}')
                else:
                    print(f'Failed to send email: {response.status_code}')
                    print(response.text)
                    return redirect('oopsy')
            else:
                print('User not found')
                return redirect('password_reset_failed')
            return redirect('password_reset_done')
    else:
        print("just empty form")
        form = CustomPasswordResetForm()

    return render(request, 'auth/password_reset_form.html', {'form': form})
    # ........................................................................

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
        print(f"Password change form is invalid. Errors: {form.errors}")

        print('###################################')
        print(f'Form errors: {form.errors}')
        print('###################################')

        return JsonResponse({'message': 'form invalid', 'errors': form.errors}, status=400)

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.user
        print(f"user ##### : {user}")
        try:
            # article_path = reverse('contact')
            # article_url = f"{self.request.scheme}://{self.request.get_host()}{article_path}"
            email_response = password_reset_complete_email(request=self.request, user=user) #, article_url=article_url)

            if email_response.status_code == 201:
                print(f'Email sent successfully to {user.email}')
            else:
                print(f'Failed to send email: {email_response.status_code}')
                print(email_response.text)
        except Exception as e:
            print(f"Error during sending password change email: {str(e)}")

        return response

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'
    # def dispatch(self, request, *args, **kwargs):
        # try:
        #     uidb64 = self.request.session.get('uidb64')
        #     print(f"uidb64: {uidb64}")
        #     if uidb64 is not None:
        #         uid = urlsafe_base64_decode(uidb64).decode()
        #         print(f"uid: {uid}")
        #         user = get_object_or_404(User, pk=uid)
        #         print(f"user: {user}")
        #         response = password_reset_complete_email(user)
        #         if response.status_code == 201:
        #             print(f'Email sent successfully to {user.email}')
        #         else:
        #             print(f'Failed to send email: {response.status_code}')
        #             print(response.text)
        #     else:
        #         print("No uidb64 found in session.")
        # except Exception as e:
        #     print(f"Error during password reset email: {str(e)}")

        # return super().dispatch(request, *args, **kwargs)

def is_superuser(req_obj):
    if req_obj.user.is_authenticated and req_obj.user.is_superuser:
        return True
    return False

def feedback_contact_list_view(request):
    superuser_access = is_superuser(request)
    print(f'Access granted:', superuser_access)
    print(f'is superuser?',superuser_access )
    if not superuser_access:
        return redirect_to_login(next=request.path)
    # articles = Article.objects.all()
    # ratings = articles[::-1]
    # ratings = articles.reverse()

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
    print(f"feedbacks_paginated:", feedbacks_paginated)
    context = {
        'feedbacks': feedbacks_paginated,
        # 'ratings': ratings,
        'pgname': 'Feedback'
    }
    return render(request, 'feedback_contact_list_view.html', context)

def feedback_contact_detail_view(request, pk):
    superuser_access = is_superuser(request)
    print(f'is superuser?',superuser_access )
    print(f'Access granted:', superuser_access)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(Contact, pk=pk)
    context = {
        'feedback': feedback,
        'pgname': 'Feedback Details'
    }
    return render(request, 'feedback_contact_detail_view.html', context)

#############################################

def feedback_article_list_view(request):
    superuser_access = is_superuser(request)
    print(f'Access granted:', superuser_access)
    print(f'is superuser?',superuser_access )
    if not superuser_access:
        return redirect_to_login(next=request.path)
    # articles = Article.objects.all()
    # ratings = articles[::-1]
    # ratings = articles.reverse()
    
    feedbacks = Article.objects.all().order_by('-id')
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
    print(f"feedbacks_paginated:", feedbacks_paginated)
    context = {
        'feedbacks': feedbacks_paginated,
        'ratings': feedbacks,
        'pgname': 'Feedback'
    }
    return render(request, 'feedback_article_list_view.html', context)

def feedback_article_detail_view(request, pk):
    superuser_access = is_superuser(request)
    print(f'is superuser?',superuser_access )
    print(f'Access granted:', superuser_access)
    if not superuser_access:
        return redirect_to_login(next=request.path)

    feedback = Article.objects.prefetch_related('comments').filter(pk=pk).first()
    author = feedback.author
    article_comments = feedback.comments.all()
    # print(f"article2 #1 : {article2}")
    print(f"article #1 : {feedback}")
    print()
    # print(f"author2 #1 : {author2}")
    print(f"author #1 : {author}")
    print()
    # print(f"comments #1 : {comments2}")
    print(f"article_comments #1 : {article_comments}")
    print()

    user = request.user
    is_owner = author == user
    is_member = False
    for comment in article_comments:
        if comment.user != None and comment.user.is_active:
            is_member = True
            print(f"Commentor {comment.user.first_name} is an active member.")
        else:
            print(f"Commentor is not an active member.")

    is_owner = author == user
    # print('is_owner:', is_owner)
    context = {
        'feedback': feedback,
        # 'article': article,
        # 'is_owner': is_owner,
        # 'is_member': is_member,
        'article_comments': article_comments,
        # 'article_title': articles,
        'pgname': 'Feedback Details'
    }
    return render(request, 'feedback_article_detail_view.html', context)

#############################################

def feedback_author_reply_list_view(request):
    superuser_access = is_superuser(request)
    print(f'Access granted:', superuser_access)
    print(f'is superuser?',superuser_access )
    if not superuser_access:
        return redirect_to_login(next=request.path)
    # articles = Article.objects.all()
    # ratings = articles[::-1]
    # ratings = articles.reverse()
    
    feedbacks = Author_reply.objects.all().order_by('-id')
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
    print(f"feedbacks_paginated:", feedbacks_paginated)
    context = {
        'feedbacks': feedbacks_paginated,
        # 'ratings': ratings,
        'pgname': 'Feedback'
    }
    return render(request, 'feedback_author_reply_list_view.html', context)

def feedback_author_reply_detail_view(request, pk):
    superuser_access = is_superuser(request)
    print(f'is superuser?',superuser_access )
    print(f'Access granted:', superuser_access)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(Author_reply, pk=pk)
    context = {
        'feedback': feedback,
        'pgname': 'Feedback Details'
    }
    return render(request, 'feedback_author_reply_detail_view.html', context)

#############################################

def feedback_comment_list_view(request):
    superuser_access = is_superuser(request)
    print(f'Access granted:', superuser_access)
    print(f'is superuser?',superuser_access )
    if not superuser_access:
        return redirect_to_login(next=request.path)
    # articles = Article.objects.all()
    # ratings = articles[::-1]
    # ratings = articles.reverse()
    
    feedbacks = Comment.objects.all().order_by('-id')
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
    print(f"feedbacks_paginated:", feedbacks_paginated)
    context = {
        'feedbacks': feedbacks_paginated,
        # 'ratings': ratings,
        'pgname': 'Feedback'
    }
    return render(request, 'feedback_comment_list_view.html', context)

def feedback_comment_detail_view(request, pk):
    superuser_access = is_superuser(request)
    print(f'is superuser?',superuser_access )
    print(f'Access granted:', superuser_access)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(Comment, pk=pk)
    context = {
        'feedback': feedback,
        'pgname': 'Feedback Details'
    }
    return render(request, 'feedback_comment_detail_view.html', context)

#############################################

def feedback_user_list_view(request):
    superuser_access = is_superuser(request)
    print(f'Access granted:', superuser_access)
    print(f'is superuser?',superuser_access )
    if not superuser_access:
        return redirect_to_login(next=request.path)
    # articles = Article.objects.all()
    # ratings = articles[::-1]
    # ratings = articles.reverse()
    
    feedbacks = User.objects.all().order_by('-id')
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
    print(f"feedbacks_paginated:", feedbacks_paginated)
    context = {
        'feedbacks': feedbacks_paginated,
        # 'ratings': ratings,
        'pgname': 'Feedback'
    }
    return render(request, 'feedback_user_list_view.html', context)

def feedback_user_detail_view(request, pk):
    superuser_access = is_superuser(request)
    print(f'is superuser?',superuser_access )
    print(f'Access granted:', superuser_access)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    feedback = get_object_or_404(User, pk=pk)
    _is_active = feedback.is_active
    _is_staff = feedback.is_staff
    _is_superuser = feedback.is_superuser
    _profile_picture = feedback.profile_picture.url
    print(f'user object: {feedback}')
    print(f'user active: {feedback.is_active}')
    print(f'user staff: {feedback.is_staff}')
    print(f'user superuser: {feedback.is_superuser}')
    print(f'user profile_picture: {feedback.profile_picture}')
    print(f'user profile_picture: {feedback.profile_picture.url}')
    context = {
        'feedback': feedback,
        'is_active': _is_active,
        'is_staff': _is_staff,
        'is_superuser': _is_superuser,
        'profile_picture': _profile_picture,
        'pgname': 'Feedback Details'
    }
    return render(request, 'feedback_user_detail_view.html', context)

#############################################

def feedback_search_history_list_view(request):
    superuser_access = is_superuser(request)
    print(f'Access granted:', superuser_access)
    print(f'is superuser?',superuser_access )
    if not superuser_access:
        return redirect_to_login(next=request.path)
    # articles = Article.objects.all()
    # ratings = articles[::-1]
    # ratings = articles.reverse()
    
    feedbacks = SearchHistory.objects.all().order_by('-id')
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
    print(f"feedbacks_paginated:", feedbacks_paginated)
    context = {
        'feedbacks': feedbacks_paginated,
        # 'ratings': ratings,
        'pgname': 'Feedback'
    }
    return render(request, 'feedback_search_history_list_view.html', context)

# def feedback_search_history_detail_view(request, str):
#     superuser_access = is_superuser(request)
#     print(f'is superuser?',superuser_access )
#     print(f'Access granted:', superuser_access)
#     if not superuser_access:
#         return redirect_to_login(next=request.path)
#     # return redirect('advanced_search', str)
#     feedback = get_object_or_404(SearchHistory, pk=pk)
#     context = {
#         'feedback': feedback,
#         'pgname': 'Feedback Details'
#     }
#     return render(request, 'feedback_search_history_detail_view.html', context)


#############################################

def feedback_list_view(request):
    superuser_access = is_superuser(request)
    print(f'is superuser?',superuser_access )
    print(f'Access granted:', superuser_access)
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
    return render(request, 'feedback_list_view.html', context)

######################
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
######################

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
