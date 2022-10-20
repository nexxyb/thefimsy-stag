# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.IndexView.as_view(), name='home'),
    
    #path('company/dashboard', views.CompanyIndexView.as_view(), name='dashboard'),
    path('expense/add', views.CreateExpenseView.as_view(), name='expense-add'),
    #path('company/<pk>/', views.CompanyDetail.as_view(), name='company-detail'),
    path('income/add', views.CreateIncomeView.as_view(), name='income-add'),
    path('project/add', views.CreateProject.as_view(), name='project-add'),
    path('expense/all', views.AllExpensesView.as_view(), name='all-expenses'),
    path('income/all', views.AllIncomesView.as_view(), name='all-incomes'),
    path('project/all', views.ProjectList.as_view(), name='all-projects'),
    path('expense/<str:pk>', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('income/<str:pk>', views.IncomeDetailView.as_view(), name='income-detail'),
    path('project/<slug:slug>', views.ProjectDetail.as_view(), name='project-detail'),
    path('expense/<str:pk>/update', views.UpdateExpenseView.as_view(), name='expense-update'),
    path('income/<str:pk>/update', views.UpdateIncomeView.as_view(), name='income-update'),
    path('project/<slug:slug>/update', views.UpdateProject.as_view(), name='project-update'),
    path('expense/<str:pk>/delete', views.DeleteExpenseView.as_view(), name='expense-delete'),
    path('income/<str:pk>/delete', views.DeleteIncomeView.as_view(), name='income-delete'),
    path('project/<slug:slug>/delete', views.DeleteProject.as_view(), name='project-delete'),
    path("contact", views.contact, name="contact"),

]
