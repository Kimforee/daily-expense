from decimal import Decimal
from .models import Expense, ExpenseSplit

def generate_balance_sheet(user):
    expenses = Expense.objects.filter(participants=user)
    total_balance = Decimal('0.00')
    individual_expenses = []

    for expense in expenses:
        # Get the amount the user owes for each expense
        split = ExpenseSplit.objects.get(expense=expense, user=user)
        balance = split.amount_owed
        total_balance += balance

        individual_expenses.append({
            'description': expense.description,
            'amount': expense.amount,
            'user_balance': balance,
            'created_at': expense.created_at,
        })

    return {
        'total_balance': total_balance,
        'individual_expenses': individual_expenses
    }
