# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from urllib import request
from django import template, forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense, Income, Project
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from .decorators import pm_required, apm_required
from django.shortcuts import redirect, render
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

User= get_user_model()
    
@method_decorator(apm_required, name='dispatch')
class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/index.html'
    model= Expense    
    
    def get_context_data(self, **kwargs):
         # Call the base implementation first to get a context
        context=super(IndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all other contexts
        context['expense_list']=Expense.objects.filter(user=self.request.user).order_by('-date')[:5]
        context['income_list']=Income.objects.filter(user=self.request.user).order_by('-date')[:5]
        project_list = Project.objects.filter(user=self.request.user).order_by('-updated')
        context['project_list'] = project_list
        context['current_user']= self.request.user.first_name
        context['project_count'] = Project.objects.filter(user=self.request.user).count()
        #context[amount_spent]= amount_spent(project_name)
        return context

# @method_decorator(pm_required, name='dispatch')
# class CompanyIndexView(LoginRequiredMixin, generic.TemplateView):
#     template_name = 'home/index2.html'
#     model= Expense    
    
#     def get_context_data(self, **kwargs):
#          # Call the base implementation first to get a context
#         context=super(CompanyIndexView, self).get_context_data(**kwargs)
#         # Add in a QuerySet of all other contexts
#         context['expense_list']=Expense.objects.filter(company_code=self.request.user).order_by('-date')[:5]
#         context['income_list']=Income.objects.filter(company_code=self.request.user).order_by('-date')[:5]
#         project_list = Project.objects.filter(company_code=self.request.user).order_by('-updated')
#         context['project_list'] = project_list
#         context['current_user']= self.request.user.first_name
#         context['project_count'] = Project.objects.filter(company_code=self.request.user).count()
#         #context[amount_spent]= amount_spent(project_name)
#         return context
    
class ExpenseDetailView(LoginRequiredMixin,generic.DetailView):
    model = Expense

class IncomeDetailView(LoginRequiredMixin,generic.DetailView):
    model = Income  

class CreateExpenseView(CreateView, LoginRequiredMixin):
    model= Expense
    fields= ['category', 'amount', 'date', 'description', 'project_name']
    
    
    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['project_name'].limit_choices_to = {'user': self.request.user}
        modelform.base_fields['date'].widget= forms.DateInput(attrs={'type': 'date'})
        modelform.base_fields['description'].widget= forms.Textarea(attrs={'rows':2, 'cols':15})
        return modelform
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.company_code = self.request.user
        return super().form_valid(form)

class UpdateExpenseView(UpdateView, LoginRequiredMixin):
    model= Expense
    fields= ['category', 'amount', 'date', 'description', 'project_name']
    
    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['project_name'].limit_choices_to = {'user': self.request.user}
        modelform.base_fields['date'].widget= forms.DateInput(attrs={'type': 'date'})
        modelform.base_fields['description'].widget= forms.Textarea(attrs={'rows':2, 'cols':15})
        return modelform
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.company_code = self.request.user
        return super().form_valid(form)
    
class DeleteExpenseView(DeleteView, LoginRequiredMixin):
    model= Expense
    success_url= reverse_lazy('all-expenses')
    
class CreateIncomeView(CreateView, LoginRequiredMixin):
    model= Income
    fields= ['category', 'amount', 'date', 'description', 'project_name']
    
    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['project_name'].limit_choices_to = {'user': self.request.user}
        modelform.base_fields['date'].widget= forms.DateInput(attrs={'type': 'date'})
        modelform.base_fields['description'].widget= forms.Textarea(attrs={'rows':2, 'cols':15})
        return modelform
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.company_code = self.request.user
        return super().form_valid(form)
    
class UpdateIncomeView(UpdateView, LoginRequiredMixin):
    model= Income
    fields= '__all__'
    
    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['project_name'].limit_choices_to = {'user': self.request.user}
        modelform.base_fields['date'].widget= forms.DateInput(attrs={'type': 'date'})
        modelform.base_fields['description'].widget= forms.Textarea(attrs={'rows':2, 'cols':15})
        return modelform
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.company_code = self.request.user
        return super().form_valid(form)
    
class DeleteIncomeView(DeleteView, LoginRequiredMixin):
    model= Income
    success_url= reverse_lazy('all-incomes')
    
class AllExpensesView(generic.ListView, LoginRequiredMixin):
    template_name = 'home/all_expenses.html'
    model= Expense
    paginate_by = 10
    
class AllIncomesView(generic.ListView, LoginRequiredMixin):
    template_name = 'home/all_incomes.html'
    model= Income
    paginate_by = 10
    
class CreateProject(CreateView, LoginRequiredMixin):
    model= Project
    fields= ['project_name', 'project_amount', 'description', 'start_date', 'end_date']
    
    def get_absolute_url(self):
        return reverse_lazy("project-detail", args=[str(self.project_id)])
    
    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['start_date'].widget= forms.DateInput(attrs={'type': 'date'})
        modelform.base_fields['end_date'].widget= forms.DateInput(attrs={'type': 'date'})
        modelform.base_fields['description'].widget= forms.Textarea(attrs={'rows':2, 'cols':15})
        return modelform
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.save()
        return super().form_valid(form)
    
        
    
class UpdateProject(UpdateView, LoginRequiredMixin):
    model= Project
    fields= ['project_amount', 'description', 'start_date', 'end_date']
    
class DeleteProject(DeleteView, LoginRequiredMixin):
    model= Project
    success_url= 'all-projects'
 
class ProjectList(generic.ListView, LoginRequiredMixin):
    model= Project
    template_name= 'home/all_projects.html'  
class ProjectDetail(generic.DetailView, LoginRequiredMixin):
    model= Project
    
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Web app feedback" 
            body = {
			'name': form.cleaned_data['name'],			 
			'message':form.cleaned_data['message'], 
			}
            email= form.cleaned_data['email_address'][0]
            message = "\n".join(body.values())

        try:
            send_mail(subject, message, 'platinexdesigns@gmail.com', [email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.') #add this
			     
    form = ContactForm()
    return render(request, "home/contact.html", {'form':form})