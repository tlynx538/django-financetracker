from django.shortcuts import render,redirect
from .models import ExpenseInfo
from django.db.models import Q,Sum
import  matplotlib.pyplot as plt
import matplotlib
import numpy as np
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout,login,authenticate
matplotlib.use('Agg')
# Create your views here.
def index(request):
	expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
	try:
        	budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
        	expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
        	fig,ax=plt.subplots()
       		ax.bar(['Expenses','Budget'], [abs(expense_total['expenses']),budget_total['budget']],color=['red','green'])
        	ax.set_title('Your total expenses vs total budget')
        	plt.savefig('main/static/main/expense.jpg')
	except TypeError:
        	print('No data.')

	context = {'expense_items':expense_items,'budget':budget_total['budget'],'expenses':expense_total['expenses']}
	return render(request,'main/index.html',context=context)
	
def login(request):
	return render(request,'registrations/login.html')


def add_item(request):
	name = request.POST['expense_name']
	expense_cost = request.POST['cost']
	expense_date = request.POST['expense_date']
	ExpenseInfo.objects.create(expense_name=name,cost=expense_cost,date_added=expense_date,user_expense=request.user)
	budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filet=Q(cost__gt=0)))
	expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
	fig,ax=plt.subplots()
	ax.bar(['Expenses','Budget'],[expense_total['expenses'],budget_total['budget']],color=['red','green'])
	ax.set_title('Your total expenses vs. Total Budget')
	plt.savefig('main/static/main/expense.jpg')
	return HttpResponseRedirect('index')

def logout_view(request):
	logout(request)
	return redirect('/')

def sign_up(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user=form.save()
			'''
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username,password=password)
			'''
			login(request,user)
			return HttpResponseRedirect('app')
		else:
			for msg in form.error_messages:
				print(form.error_messages[msg])
	form = UserCreationForm()
	return render(request, 'main/sign_up.html',{'form':form})
