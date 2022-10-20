# shop/management/commands/populate_db.py

import random
from datetime import datetime, timedelta
from secrets import choice

import pytz
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.home.models import Project, Expense, Income
from apps.authentication.models import User


class Command(BaseCommand):
    help = 'Populates the database with random generated data.'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The number of purchases that should be created.')

    def handle(self, *args, **options):
        dt1 = pytz.utc.localize(datetime.now() - timedelta(days=random.randint(0, 1825)))
        dt2 = dt1  + timedelta(days=random.randint(0, 1825))
        user= User.objects.get(id=1)
        projects = [
            Project.objects.create(project_name='Socks', start_date=dt1, end_date= dt2, user= user, project_amount=65000), Project.objects.create(project_name='Pants', start_date=dt1, end_date= dt2, user= user, project_amount=120000),
            Project.objects.create(project_name='T-Shirt', start_date=dt1, end_date= dt2, user= user, project_amount=800000), Project.objects.create(project_name='Boots', start_date=dt1, end_date= dt2, user= user, project_amount=90000),
         ]
        amount = options['amount'] if options['amount'] else 2500
        project_choice= Project.objects.get(user=user)[0]
        for i in range(0, amount):
            dt = pytz.utc.localize(datetime.now() - timedelta(days=random.randint(0, 1825)))
            expense = Expense.objects.create(
                category =random.choice(Expense.category)[0],
                amount = random.randint(200, 1500),
                date= dt,
                project_name= random.choice(project_choice),
                user=user,
            )            
            income = Income.objects.create(
                category =random.choice(Income.category)[0],
                amount = random.randint(200, 1500),
                date= dt,
                project_name= random.choice(project_choice),
                user=user,
                )
        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))
