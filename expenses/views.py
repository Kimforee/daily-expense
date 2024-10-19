from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from .models import Expense
from .serializers import ExpenseSerializer

# View for creating a new user
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# View for retrieving user details
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'  # Fetch user by primary key (id)

class AddExpenseView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class UserExpensesView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(participants=user)

class AllExpensesView(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
