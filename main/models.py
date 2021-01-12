from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class AccountInfo(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	user_budget = models.IntegerField()
	
	def __str__(self):
		return self.username



class BudgetInfo(models.Model):
	user_budget=models.IntegerField()
	expenses = models.IntegerField()
	category = models.CharField(max_length=10)
	user = models.ForeignKey(AccountInfo, on_delete=models.CASCADE)



class ExpenseInfo(models.Model):
	expense_name = models.TextField(default='Test')
	expenses = models.IntegerField(default=0)
	cost = models.FloatField(default=0)
	date_added = models.DateField(default="1960-01-01")
	user_expense = models.ForeignKey(User, on_delete=models.CASCADE)