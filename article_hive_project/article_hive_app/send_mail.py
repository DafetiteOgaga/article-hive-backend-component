import os, sys, requests, base64 #, json
from django.template.loader import render_to_string
from django.urls import reverse
# from .logo import article_hive_logo

sys.path.append(os.path.expanduser("~"))
from mhykhehy import api_key
# print(f"my key: {api_key}")
url = 'https://api.brevo.com/v3/smtp/email'

# img = "static/article_hive_project/logo - shade of brown/the-article-hive-high-resolution-logo-transparent.png"
# print('is img correct?', os.path.isfile(img))

with open("static/article_hive_project/logo - shade of brown/the-article-hive-high-resolution-logo-transparent.png", "rb") as image_file:
		encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

def req(request):
	article_support_url = reverse('contact')
	return f"{request.scheme}://{request.get_host()}{article_support_url}"

def send_password_reset_email(request: object, user: object, reset_link: str):
	subject = render_to_string('emails/password_reset_subject.txt', {'user': user}).strip()
	email_body = render_to_string('emails/password_reset_email.html', {
		'user': user.first_name,
		'reset_link': reset_link,
		'article_support_url': req(request=request),
		# 'article_hive_logo': article_hive_logo,
		'heading': 'Password Reset Request'
	})

	# print(f"user: {user}")
	# print(f"email: {user.email}")
	# print(f"firstname: {user.first_name}")
	# print(f"subject: {subject}")
	# print(f"reset link: {reset_link}")

	email_data = {
		'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
		'to': [{'email': user.email, 'name': user.first_name}],
		'subject': subject,
		'htmlContent': f'{email_body}',
		'textContent': f'Password Reset Link: {reset_link}',
		'attachment': [
			{
				'content': encoded_image,
				'name': 'logo.png',
				'contentType': 'image/png',
			},
		],
	}

	# Request headers
	headers = {
		'accept': 'application/json',  # Accept JSON response
		'api-key': api_key,  # API key header
		'content-type': 'application/json'  # Content type header
	}

	response = requests.post(url, headers=headers, json=email_data) # , data=json.dumps(email_data))
	return response


def welcome_email(request: object, user: object, article_url: str):
	subject = render_to_string('emails/welcome_subject.txt', {'user': user}).strip()
	email_body = render_to_string('emails/welcome_email.html', {
		'user': user.first_name,
		'article_url': article_url,
		'article_support_url': req(request=request),
		# 'article_hive_logo': article_hive_logo,
		'heading': 'Welcome to Article Hive'
	})

	# print(f"user: {user}")
	# print(f"email: {user.email}")
	# print(f"firstname: {user.first_name}")
	# print(f"article_url: {article_url}")
	# print(f"subject: {subject}")
	# # print(f"reset link: {reset_link}")

	email_data = {
		'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
		'to': [{'email': user.email, 'name': user.first_name}],
		'subject': subject,
		'htmlContent': f'{email_body}',
		'textContent': f'Welcome to Article Hive',
		'attachment': [
			{
				'content': encoded_image,
				'name': 'logo.png',
				'contentType': 'image/png',
			},
		],
	}

	# Request headers
	headers = {
		'accept': 'application/json',
		'api-key': api_key,
		'content-type': 'application/json'
	}

	response = requests.post(url, headers=headers, json=email_data) # , data=json.dumps(email_data))
	return response

def comment_notification_email(request: object, comment_author: str, comment: object, article_url: str):
	subject = render_to_string('emails/comment_subject.txt', {'user': comment.article.author}).strip()
	email_body = render_to_string('emails/comment_email.html', {
		'comment_author': comment_author,
		'comment': comment,
		'article_url': article_url,
		'article_support_url': req(request=request),
		# 'article_hive_logo': article_hive_logo,
		'heading': 'New Comment on Your Article'
		# 'heading': 'Comment to your Article'
	})

	# print(f"##################### comment #####################")
	# print(f"user: {comment.article.author}")
	# print(f"title: {comment.article.title}")
	# print(f"email: {comment.article.author.email}")
	# print(f"comment_author: {comment_author}")
	# print(f"comment: {comment}")
	# print(f"article: {comment.article}")
	# print(f"article_url: {article_url}")
	# print(f"firstname: {comment.article.author.first_name}")
	# print(f"subject: {subject}")
	# # print(f"reset link: {reset_link}")
	# print(f"#####################  #####################")

	email_data = {
		'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
		'to': [{'email': comment.article.author.email, 'name': comment.article.author.first_name}],
		'subject': subject,
		'htmlContent': f'{email_body}',
		'textContent': f'Comment to Article Hive',
		'attachment': [
			{
				'content': encoded_image,
				'name': 'logo.png',
				'contentType': 'image/png',
			},
		],
	}

	# Request headers
	headers = {
		'accept': 'application/json',
		'api-key': api_key,
		'content-type': 'application/json'
	}

	response = requests.post(url, headers=headers, json=email_data) # , data=json.dumps(email_data))
	return response

def author_reply_notification_email(request: object, reply: object, article_url: str):
	subject = render_to_string('emails/response_to_comment_subject.txt', {'reply': reply}).strip()
	email_body = render_to_string('emails/response_to_comment_email.html', {
		'reply': reply,
		'article_url': article_url,
		'article_support_url': req(request=request),
		# 'article_hive_logo': article_hive_logo,
		'heading': f'Response to your comment on {reply.comment.article.title}'
		# 'heading': 'Comment to your Article'
	})

	# print(f"##################### reply #####################")
	# print(f"user: {reply.comment.article.author}")
	# print(f"title: {reply.comment.article.title}")
	# print(f"email: {reply.comment.article.author.email}")
	# print(f"comment_author: {reply.comment.user.first_name}")
	# print(f"commentor_email: {reply.comment.user.email}")
	# print(f"reply: {reply}")
	# print(f"article: {reply.comment.article}")
	# print(f"article_url: {article_url}")
	# print(f"firstname: {reply.comment.article.author.first_name}")
	# print(f"subject: {subject}")
	# # print(f"reset link: {reset_link}")
	# print(f"#####################  #####################")

	email_data = {
		'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
		'to': [{'email': reply.comment.user.email, 'name': reply.comment.user.first_name}],
		'subject': subject,
		'htmlContent': f'{email_body}',
		'textContent': f'Response to your comment',
		'attachment': [
			{
				'content': encoded_image,
				'name': 'logo.png',
				'contentType': 'image/png',
			},
		],
	}

	# Request headers
	headers = {
		'accept': 'application/json',
		'api-key': api_key,
		'content-type': 'application/json'
	}

	response = requests.post(url, headers=headers, json=email_data) # , data=json.dumps(email_data))
	return response

def password_reset_complete_email(request: object, user: object):
	subject = render_to_string('emails/password_reset_complete_subject.txt', {'user': user}).strip()
	email_body = render_to_string('emails/password_reset_complete_email.html', {
		'user': user.first_name,
		# 'article_url': article_url,
		'article_support_url': req(request=request),
		# 'article_hive_logo': article_hive_logo,
		'heading': f'Password Reset Successful',
		# 'heading': 'Comment to your Article'
	})

	# print(f"##################### reset #####################")
	# print(f"user: {user}")
	# print(f"email: {user.email}")
	# print(f"first name: {user.first_name}")
	# print(f"subject: {subject}")
	# # print(f"reset link: {reset_link}")
	# print(f"#####################  #####################")

	email_data = {
		'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
		'to': [{'email': user.email, 'name': user.first_name}],
		'subject': subject,
		'htmlContent': f'{email_body}',
		'textContent': f'Reset Password Successful',
		'attachment': [
			{
				'content': encoded_image,
				'name': 'logo.png',
				'contentType': 'image/png',
			},
		],
	}

	# Request headers
	headers = {
		'accept': 'application/json',
		'api-key': api_key,
		'content-type': 'application/json'
	}

	response = requests.post(url, headers=headers, json=email_data) # , data=json.dumps(email_data))
	return response

def password_change_done_email(request: object, user: object):
	subject = render_to_string('emails/password_change_done_subject.txt', {'user': user}).strip()

	# with open("static/article_hive_project/logo - shade of brown/the-article-hive-high-resolution-logo-transparent.png", "rb") as image_file:
	# 	encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

	email_body = render_to_string('emails/password_change_done_email.html', {
		'user': user.first_name,
		# 'article_url': article_url,
		'article_support_url': req(request=request),
		# 'article_hive_logo': article_hive_logo,
		'heading': f'Password Change Successful',
		# 'heading': 'Comment to your Article'
	})

	# print(f"##################### change #####################")
	# print(f"user: {user}")
	# print(f"email: {user.email}")
	# print(f"first name: {user.first_name}")
	# print(f"subject: {subject}")
	# # print(f"reset link: {reset_link}")
	# print(f"#####################  #####################")

	email_data = {
		'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
		'to': [{'email': user.email, 'name': user.first_name}],
		'subject': subject,
		'htmlContent': f'{email_body}',
		'textContent': f'Password Change Successful',
		'attachment': [
			{
				'content': encoded_image,
				'name': 'logo.png',
				'contentType': 'image/png',
			},
		],
	}

	# Request headers
	headers = {
		'accept': 'application/json',
		'api-key': api_key,
		'content-type': 'application/json'
	}

	response = requests.post(url, headers=headers, json=email_data) # data=json.dumps(email_data))
	# print(f"Response status: {response.status_code}")
	# print(f"Response content: {response.text}")
	return response

def congratulations_first_post(request: object, user: object, article_url: str):
	subject = render_to_string('emails/congratulations_first_post_subject.txt', {'user': user}).strip()
	email_body = render_to_string('emails/congratulations_first_post_email.html', {
		'user': user.first_name,
		'article_url': article_url,
		'article_support_url': req(request=request),
		# 'article_hive_logo': article_hive_logo,
		'heading': f'Congratulations on your First Post',
		# 'heading': 'Comment to your Article'
	})

	# print(f"##################### congratulations #####################")
	# print(f"user: {user}")
	# print(f"email: {user.email}")
	# print(f"first name: {user.first_name}")
	# print(f"subject: {subject}")
	# # print(f"reset link: {reset_link}")
	# print(f"#####################  #####################")

	email_data = {
		'sender': {'name': 'Article-Hive', 'email': 'ogagadafetite@gmail.com'},
		'to': [{'email': user.email, 'name': user.first_name}],
		'subject': subject,
		'htmlContent': f'{email_body}',
		'textContent': f'First Post',
		'attachment': [
			{
				'content': encoded_image,
				'name': 'logo.png',
				'contentType': 'image/png',
			},
		],
	}

	# Request headers
	headers = {
		'accept': 'application/json',
		'api-key': api_key,
		'content-type': 'application/json'
	}

	response = requests.post(url, headers=headers, json=email_data) # , data=json.dumps(email_data))
	return response
