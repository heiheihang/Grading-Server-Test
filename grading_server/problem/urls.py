from django.urls import path

from problem import views

urlpatterns = [
    path('', views.problem_index_view, name='problem_index'),
    path('create/', views.problem_create_view, name='problem_create'),
    path('<int:problem_id>/', views.problem_view, name='problem'),
    path('<int:problem_id>/edit/', views.problem_edit_view, name='problem_edit'),
    path('<int:problem_id>/<int:suite_id>/create', views.test_suite_create_view, name='suite_create'),
    path('<int:problem_id>/<int:suite_id>/<int:pair_id>/create',views.test_pair_create_view, name='pair_create')
]
