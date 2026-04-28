from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('salaries/', views.salary_insights, name='salary_insights'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
]