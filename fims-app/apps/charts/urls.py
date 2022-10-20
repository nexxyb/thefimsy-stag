from django.contrib import admin
from django.urls import path, include
from apps.charts import views

path('charts/', views.charts_view, name='charts'),
path('chart/expense/filter-options/', views.get_expense_filter_options, name='expense-chart-filter-options'),
path('chart/income/filter-options/', views.get_income_filter_options, name='income-chart-filter-options'),
path('chart/expense/year/<int:year>/', views.get_expense_year_chart, name='expense-chart-year'),
