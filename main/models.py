from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
'''
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
'''
class ExpenseInfo(models.Model):
	expenses = models.IntegerField()
	cost = models.FloatField()
	date_added = models.DateField()
	user_expense = models.ForeignKey(User, on_delete=models.CASCADE)


