from django.urls import path

from submission import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subs/', views.submissions, name='subs'),
]
