from django.urls import path
from .views import ReportHome, ExpenseReport, IncomeReport, report

urlpatterns = [
    path('report/', ReportHome.as_view(), name='report'),
    path('report/expense', ExpenseReport.as_view(), name='expense-report'),
    path('report/income', IncomeReport.as_view(), name='income-report'),
    path('report/project', report, name='project-report'),
]
