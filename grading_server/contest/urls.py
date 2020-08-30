from django.urls import path

from contest import views

urlpatterns = [
    path('', views.contest_index_view, name='contest_index'),
    path('create/', views.contest_create_view, name='contest_create'),
    path('<int:contest_id>/', views.contest_detail_view, name='contest_detail'),
    path('<int:contest_id>/edit/', views.contest_edit_view, name='contest_edit'),
    path('<int:contest_id>/register/', views.contest_register_view, name='contest_register'),
    path('<int:contest_id>/edit/add_problem/', views.contest_add_problem_view, name='add_problem'),
]
