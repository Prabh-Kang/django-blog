from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.BlogHomeView.as_view(), name='blog-home'),
    path('detail/<int:pk>/', views.BlogDetailView.as_view(), name='detail-view'),
    path('register/', views.registerPage, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blogapp/login.html'), name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('profile/', views.profilePage, name='profile'),
    path('create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('update/<int:pk>/', views.BlogUpdateView.as_view(), name='blog-update'),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name='blog-delete'),
    path('userbloglist/<int:pk>/', views.UserBlogListView.as_view(), name='user-blog-list'),
    path('mybloglist/', views.MyBlogListView.as_view(), name='my-blog-list'),
    path('testpage/<int:pk>/', views.testpage, name='testpage'),
    path('ajaxx/', views.ajaxcomments, name='testcommentpage'),


      # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

]