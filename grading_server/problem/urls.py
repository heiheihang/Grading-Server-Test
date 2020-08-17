from django.urls import path

from problem import views

urlpatterns = [
    path('', views.problem_index_view, name='problem_index'),
    path('create/', views.problem_create_view, name='problem_create'),
    path('<int:problem_id>/', views.problem_view, name='problem'),
    path('<int:problem_id>/edit/', views.problem_edit_view, name='problem_edit'),
    path('<int:problem_id>/<int:suite_id>/', views.test_suite_detail_view, name='suite_detail'),
    path('<int:problem_id>/<int:suite_id>/delete', views.test_suite_delete_view, name='delete_suite'),
    path('<int:problem_id>/<int:suite_id>/new_test',views.test_pair_create_view, name='pair_create'),
    path('<int:problem_id>/<int:suite_id>/<int:pair_id>/delete',views.test_pair_delete_view, name='pair_delete'),
    path('<int:problem_id>/edit/new_suite',views.test_suite_create_view, name='new_suite')
]
