from django.shortcuts import render, redirect
from .models import ExpenseInfo, BudgetInfo
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate



def index(request):
	get_expenses_graph(request)
	expense_items = ExpenseInfo.objects.filter(
		user_expense=request.user
	).order_by('-date_added') or {}
	
	try:
		expense_total = ExpenseInfo.objects.filter(
			user_expense=request.user
		).aggregate(budget=Sum('cost'))
		
		if not expense_total['budget']:
			expense_total['budget'] = "00"
	except Exception:
		expense_total['budget'] = "0.00"

	context = {
		'expense_items': expense_items,
		'expenses': expense_total['budget']
	}
	return render(request,'main/index.html',context=context)



def add_item(request):
	name = request.POST['expense_name']
	expense_cost = request.POST['cost']
	expense_date = request.POST['expense_date']

	new_expense = ExpenseInfo.objects.create(
		expense_name=name,
		cost=expense_cost,
		date_added=expense_date,
		user_expense=request.user
	)
	new_expense.save()

	return HttpResponseRedirect('app')



def logout_view(request):
	logout(request)
	return redirect('/')



def sign_up(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user=form.save()
			login(request,user)
			return HttpResponseRedirect('app')
		else:
			for msg in form.error_messages:
				print(form.error_messages[msg])
	form = UserCreationForm()
	return render(request, 'main/sign_up.html',{'form':form})



def get_expenses_graph(request):
	"""
	Calculates all the user's monthly expenditures.
	"""
	response = {
		"days": [],
		"expenditures": []
	}

	all_user_expenes = ExpenseInfo.objects.filter(
		user_expense=request.user
	).order_by("-date_added")

	if not all_user_expenes:
		return JsonResponse(response)
	
	for expense in all_user_expenes:
		day = expense.date_added
		cost = expense.cost
		response['days'].append(day)
		response['expenditures'].append(cost)

	return JsonResponse(response)