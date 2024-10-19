# expenses/urls.py
from django.urls import path
from .views import UserCreateView, UserDetailView, AddExpenseView, UserExpensesView, AllExpensesView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('expenses/', AddExpenseView.as_view(), name='add-expense'),
    path('expenses/user/', UserExpensesView.as_view(), name='user-expenses'),
    path('expenses/all/', AllExpensesView.as_view(), name='all-expenses'),
]
