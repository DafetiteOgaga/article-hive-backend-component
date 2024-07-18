from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
	# Create your urlpatterns here.
	path('', views.home, name='home'),
	path('hive/', views.hive, name='hive'),
	path('about/', views.about_page, name='about'),
	path('contact/', views.contact_page, name='contact'),
	path('profile/<int:pk>/', views.profile_page, name='profile'),
	path('profile-update/<int:pk>/', views.profile_update, name='profile_update'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),
	path('register/', views.register_page, name='register'),

	# path('article/new/<int:pk>/', views.article_form, name='article_form'),
	path('article/<int:pk>/', views.article, name='article'),
	path('author-response/<int:pk>/', views.author_response, name='author_response'),
	path('article/new/', views.article_form, name='article_form'),
	path('update-article-form/<int:pk>/', views.update_article_form, name='update_article_form'),
	path('member-articles/<int:pk>/', views.article_list, name='article_list'),

	path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/failed/', views.password_reset_failed_view, name='password_reset_failed'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

	path('feedback/article/', views.feedback_article_list_view, name='feedback_article_list_view'),
	path('feedback/article-detail/<int:pk>/', views.feedback_article_detail_view, name='feedback_article_detail_view'),
	path('feedback/author-reply/', views.feedback_author_reply_list_view, name='feedback_author_reply_list_view'),
	path('feedback/author-reply-detail/<int:pk>/', views.feedback_author_reply_detail_view, name='feedback_author_reply_detail_view'),
	path('feedback/comment/', views.feedback_comment_list_view, name='feedback_comment_list_view'),
	path('feedback/comment-detail/<int:pk>/', views.feedback_comment_detail_view, name='feedback_comment_detail_view'),
	path('feedback/contact/', views.feedback_contact_list_view, name='feedback_contact_list_view'),
	path('feedback/contact-detail/<int:pk>/', views.feedback_contact_detail_view, name='feedback_contact_detail_view'),
	path('feedback/user/', views.feedback_user_list_view, name='feedback_user_list_view'),
	path('feedback/user-detail/<int:pk>/', views.feedback_user_detail_view, name='feedback_user_detail_view'),
	path('feedback/search-history/', views.feedback_search_history_list_view, name='feedback_search_history_list_view'),
	# path('feedback/search-history-detail/<str:pk>/', views.feedback_search_history_detail_view, name='feedback_search_history_detail_view'),
	path('feedback/', views.feedback_list_view, name='feedback_list_view'),

	path('oopsy/', views.oopsy_view, name='oopsy'),

	path('search/', views.advanced_search, name='advanced_search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),

	path('test-email/', views.test_email_view, name='test_email'),
	# path('test-404/', lambda request: None),

	path('test_authentication/', views.test_authentication, name='test_authentication'),
	path('ports/', views.checkRequest, name='checkRequest'),
]
