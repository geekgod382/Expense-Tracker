from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum
import json

# Create your views here.
@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(exp.amount for exp in expenses)

    category_data = expenses.values('category').annotate(total = Sum('amount'))

    categories = [entry['category'] for entry in category_data]
    totals = [entry['total'] for entry in category_data]
    
    # Calculate monthly total
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_expenses = expenses.filter(date__month=current_month, date__year=current_year)
    monthly_total = sum(exp.amount for exp in monthly_expenses)
    
    return render(request, 'expenses/home.html', {
        'expenses': expenses,
        'total': total,
        'monthly_total': monthly_total,
        'totals_json' : json.dumps(totals),
        'categories_json' : json.dumps(categories)
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            return redirect('expense:home')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def logout(request):
    return render(request, 'expenses/logout.html')

@login_required
def delete(request, expense_id):
    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
        expense.delete()
        return redirect('expense:home')
    except Expense.DoesNotExist:
        return redirect('expense:home')
