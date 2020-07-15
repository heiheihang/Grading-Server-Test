from django.urls import path

from submission import views

urlpatterns = [
    path('<int:problem_id>/', views.submission_view, name='submission_view'),
    path('subs/', views.submissions, name='subs'),
    path('', views.problem_submission_index, name='submission_index')
]
