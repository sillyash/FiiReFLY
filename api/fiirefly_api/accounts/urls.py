from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='auth-login'),
    path('callback/', views.callback_view, name='auth-callback'),
    path('token/', views.token_view, name='auth-token'),
    path('logout/', views.logout_view, name='auth-logout'),
    path('me/', views.me_view, name='auth-me'),
]
