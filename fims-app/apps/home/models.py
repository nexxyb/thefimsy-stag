# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from operator import mod
from time import timezone
from unicodedata import decimal
from django.db import models
from django.db.models import Sum, Q
from datetime import date
import datetime
from django.urls import reverse
import uuid
from django.contrib.auth import get_user_model
from django.conf import settings   
from djmoney.models.fields import MoneyField
from random import randint
from django.template.defaultfilters import slugify
from moneyed import Money

NoneType = type(None)
class Project(models.Model):
    project_id= models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=45)
    project_name= models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=False, unique=True)
    project_amount=MoneyField(verbose_name='Budget', max_digits=14, decimal_places=2, default_currency='USD')
    description = models.TextField(null=True, blank=True, max_length= 200)
    start_date= models.DateField()
    end_date= models.DateField()
    #company_code=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', through="Project_Users")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,to_field='id', related_name='+', on_delete=models.CASCADE)
    updated= models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.project_name
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.project_name)
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering= ['project_name']
    
    def get_absolute_url(self):
        return reverse("project-detail", kwargs={'slug':self.slug})
    
    
    @property
    def duration(self):        
        start= date(self.start_date.year, self.start_date.month, self.start_date.day)
        end= date(self.end_date.year, self.end_date.month, self.end_date.day)
        delta = end- start
        duration = delta.days
        duration_weeks = duration/5.5
        return int(duration_weeks)
    
    def total_spent(self):
        total_spent = Expense.objects.filter(project_name=self.project_name).aggregate(total=Sum('amount'))
        spent= total_spent['total']
        if type(spent) == NoneType :
            return Money(0, self.project_amount_currency)
        else:
            return Money(spent, self.project_amount_currency)
        
    
    @property
    def total_income(self):
        total_amount = Income.objects.filter(project_name=self.project_name).aggregate(total=Sum('amount'))
        income= total_amount['total']
        if type(income) == NoneType:
            return Money(0, self.project_amount_currency)
        else:
            return Money(income, self.project_amount_currency)
        
    @property
    def budget_balance(self):
        total_spent = Expense.objects.filter(project_name=self.project_name).aggregate(total=Sum('amount'))
        if type(total_spent['total']) == NoneType:
             spent = 0
        else:
            spent= float(total_spent['total'])
        budget_query= Project.objects.get(project_name=self.project_name).project_amount.amount
        #currency_query= Project.objects.get(project_name=self.project_name).project_amount.currency
        budget= float(budget_query)
        return Money(budget - spent, self.project_amount_currency)  
        
    @property
    def actual_balance(self):
        total_spent = Expense.objects.filter(project_name=self.project_name).aggregate(total=Sum('amount'))
        if type(total_spent['total']) == NoneType:
            spent = 0
        else:
            spent= float(total_spent['total'])
        total_income = Income.objects.filter(project_name=self.project_name).aggregate(total=Sum('amount'))
        if type(total_income['total']) == NoneType :
            income_total = 0
        else:
            income_total= float(total_income['total'])
        return Money(income_total - spent, self.project_amount_currency)
    
    @property
    def progress(self):
        #spent = Project.total_spent(self)
        total_spent = Expense.objects.filter(project_name=self.project_name).aggregate(total=Sum('amount'))
        spent= total_spent['total']
        budget_query= Project.objects.get(project_name=self.project_name).project_amount.amount
        budget= float(budget_query)
        if type(spent) is not NoneType:
            progress= (float(spent) / budget) * 100
            return int(progress)
        else:
            return 0


class Expense(models.Model):
    
    EXPENSE_CHOICES=[
        (
            'Transportation', (
                ('ticket', 'Ticket'),
                ('fuel', 'Fuel'),
                ('insurance', 'Insurance'),
                ('taxi', 'Taxi'),
                ('maintenance', 'Maintenance'),
                ('flight', 'Flight')                

            )
        ),
       
        (
            'Entertainment', (
                ('dinner', 'Dinner'),
                ('party', 'Party'),
                ('sports', 'Sports'),
                ('concert', 'Concert'),
                ('other', 'Other')
            )
        ),
        (
            'Project', (
                ('salary', 'Salary'),
                ('materials', 'Materials'),
                ('workmanship', 'Workmanship'),
                ('contract', 'Contract'),
                ('training', 'Training'),
                ('commissioning', 'Commissioning')
            )
        ),
        (
            'Office', (
                ('office_supply', 'Office Supply'),
                ('office_furniture', 'Office Furniture'),
                ('stationery', 'Stationery'),
                ('internet', 'Internet'),
                ('phone', 'Phone')
            )
        )
    ]
    expense_id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=45)
    category= models.CharField(max_length=20, choices=EXPENSE_CHOICES, default='Select')
    amount=MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date=models.DateTimeField(default=datetime.datetime.today)
    description=models.TextField(max_length=200, null=True, blank=True)
    project_name= models.ForeignKey('Project', to_field='project_name', on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,to_field='id', related_name='+', on_delete=models.CASCADE)
    #company_code=models.ForeignKey(settings.AUTH_USER_MODEL, to_field='company_code', on_delete=models.CASCADE)
    #company_code=models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    def __str__(self):
        return ('Expense:{}={}').format(self.category, self.amount)
    class Meta:
        ordering= ['date']

    def get_absolute_url(self):
        return reverse("expense-detail", args=[str(self.expense_id)])
    
class Income(models.Model):
    INCOME_CHOICES=[
        ('salary', 'Salary'),
        ('equities', 'Equities'),
        ('rents_royalties', 'Rents and Royalties'),
        ('sales', 'Sales'),
        ('commission', 'Commission'),
        ('profit', 'Profit'),
        ('shares','Shares')
    ]
    income_id=models.CharField(primary_key=True, default=uuid.uuid4,  editable=False, max_length=45)
    category= models.CharField(max_length=20, choices=INCOME_CHOICES, default='Select')
    amount= MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date=models.DateTimeField(default=datetime.datetime.today)
    description=models.TextField(max_length=200, null=True, blank=True)
    project_name= models.ForeignKey('Project', to_field='project_name', on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,to_field='id', related_name='+', on_delete=models.CASCADE)
    #company_code=models.ForeignKey(settings.AUTH_USER_MODEL, to_field='company_code', on_delete=models.CASCADE)
    #company_code=models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    
    def __str__(self):
        return ('Income:{}={}').format(self.category, self.amount)
    class Meta:
        ordering= ['date']

    def get_absolute_url(self):
        return reverse("income-detail", args=[str(self.income_id)])
    
    