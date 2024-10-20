from decimal import Decimal
from .models import Expense, ExpenseSplit
from django.shortcuts import get_object_or_404
from .models import CustomUser

def generate_balance_sheet(user):
    # calculation logic
    total_owed = 0
    total_lent = 0 

    # Assuming you have access to the Expense and ExpenseSplit models
    expenses = Expense.objects.filter(creator=user)
    
    for expense in expenses:
        total_lent += expense.amount
        splits = ExpenseSplit.objects.filter(expense=expense)
        for split in splits:
            if split.user == user:
                total_owed += split.amount_owed

    net_balance = total_lent - total_owed
    return [{
        'user': user.name,
        'total_owed': total_owed,
        'total_lent': total_lent,
        'net_balance': net_balance,
    }]


def split_equal(expense, participants):
    split_amount = expense.amount / len(participants)
    splits = []
    
    for participant in participants:
        splits.append(ExpenseSplit(expense=expense, user=participant, amount_owed=split_amount))
    
    return splits

def split_exact(expense, splits_data):
    splits = []
    for user_id, amount in splits_data.items():
        # Fetch the user instance using the ID
        participant = get_object_or_404(CustomUser, id=user_id)
        splits.append(ExpenseSplit(expense=expense, user=participant, amount_owed=Decimal(amount)))
    return splits

def split_percentage(expense, percentages):
    splits = []
    
    for participant, percentage in percentages.items():
        amount_owed = expense.amount * (Decimal(percentage) / Decimal('100'))
        splits.append(ExpenseSplit(expense=expense, user=participant, amount_owed=amount_owed))
    
    return splits
