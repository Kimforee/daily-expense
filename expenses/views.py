from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, Expense, ExpenseSplit
from .serializers import UserSerializer, ExpenseSerializer, ExpenseSplitSerializer, RegistrationSerializer
from django.http import HttpResponse
from .utils import generate_balance_sheet
import csv
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm
from django.views import View
from rest_framework.permissions import AllowAny
import logging

class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")  # Log the error
            return Response({"error": True, "message": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        else:
            return render(request, 'expenses/login.html', {'error': 'Invalid email or password'})
    return render(request, 'expenses/login.html')

@login_required
def home(request):
    return render(request, 'expenses/home.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Redirect to the home page after successful login
        if response.status_code == 200:
            return HttpResponseRedirect('/')  # Redirect to home page
        return response

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class AddExpenseView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

class UserExpensesView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get_queryset(self):
        return Expense.objects.filter(participants__id=self.request.user.id)

class AllExpensesView(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

from django.http import HttpResponse
import csv

class DownloadBalanceSheetView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Check if user is authenticated
        if not user.is_authenticated:
            return Response({"error": "User not authenticated."}, status=403)

        # Get the balance sheet data for the user
        balance_data = generate_balance_sheet(user)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

        writer = csv.writer(response)
        writer.writerow(['User', 'Total Owed', 'Total Lent', 'Net Balance'])

        # Check if balance_data is structured correctly
        if not isinstance(balance_data, list):
            print("Error: balance_data is not a list.")
            return Response({"error": "Invalid balance data."}, status=500)

        # Write the data to CSV
        for item in balance_data:
            if isinstance(item, dict):  # Make sure it's a dictionary-like structure
                writer.writerow([item['user'], item['total_owed'], item['total_lent'], item['net_balance']])
            else:
                print(f"Error: item {item} is not a dict.")

        return response