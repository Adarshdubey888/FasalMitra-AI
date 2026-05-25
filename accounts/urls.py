from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('login/', views.login_user, name='login'),
    path('login-otp/', views.login_otp, name='login_otp'),

    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('admin-login/', views.admin_login, name='admin_login'),

    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
]