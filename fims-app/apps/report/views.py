from datetime import datetime
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.home.models import Expense, Income, Project
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
from django.http import FileResponse
from fpdf import FPDF

# Create your views here.
class ReportHome(LoginRequiredMixin, generic.TemplateView):
    template_name= 'report/report.html'
    
class ExpenseReport(LoginRequiredMixin, generic.TemplateView):
    pass

class IncomeReport(LoginRequiredMixin, generic.TemplateView):
    pass

def report(request):
    dt = datetime.today()
    projects = Project.objects.all()
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, f"Your projects' summary as at {dt}",0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Project'.ljust(30)} {'Total Amount Spent'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for project in projects:
        pdf.cell(200, 8, f"{project.project_name.ljust(30)} {str(project.total_spent()).rjust(20)}", 0, 1)
    pdf.output('report.pdf', 'F')
    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
    
