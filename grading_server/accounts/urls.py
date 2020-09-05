from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.custom_register, name='register'),
    path('verify/<uidb64>/<token>/', views.verify_email_view, name='verify_email'),
]
