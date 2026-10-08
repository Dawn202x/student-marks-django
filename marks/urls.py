from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.show_marks, name='show_marks'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add/', views.add_mark_view, name='add_mark'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
]