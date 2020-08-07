from django.urls import path

from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:user_id>/', views.user_view, name='user_view'),
]
