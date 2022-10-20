from django.shortcuts import render
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from .charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict

# Create your views here.

def get_expense_filter_options(request):
    grouped_expenses = Expense.objects.filter(user=request.user).annotate(year=ExtractYear('date')).values('year').order_by('-year').distinct()
    options = [expense['year'] for expense in grouped_expenses]

    return JsonResponse({
        'options': options,
    })

def get_income_filter_options(request):
    grouped_incomes = Income.objects.filter(user=request.user).annotate(year=ExtractYear('date')).values('year').order_by('-year').distinct()
    options = [income['year'] for income in grouped_incomes]

    return JsonResponse({
        'options': options,
    })
    
def get_expense_year_chart(request, year):
    expenses = Expense.objects.filter(date__year=year)
    grouped_expenses = expenses.filter(user=request.user).annotate(Total=F('amount')).annotate(month=ExtractMonth('date'))\
        .values('month').annotate(average=Sum('amount')).values('month', 'average').order_by('month')

    expense_dict = get_year_dict()

    for group in grouped_expenses:
        expense_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Total Expense in {year}',
        'data': {
            'labels': list(expense_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(expense_dict.values()),
            }]
        },
    })

def charts_view(request):
    return render(request, 'home/charts.html', {})