from django.urls import path
from django.urls import include
from django.contrib.auth import views as default_views

from . import views

urlpatterns = [
    path('login/', default_views.LoginView.as_view(), name='login'),
    path('logout/', default_views.LogoutView.as_view(), name='logout'),

    path('password_change/', default_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', default_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', default_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', default_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', default_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', default_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.my_profile, name='my_profile'),
    path('users/<int:pk>', views.profile, name='profile'),
    path('create/', views.CreateAccountView.as_view(), name='create_account'),
    path('create/done', views.create_account_done, name='create_account_done'),
]
