from django.urls import path
from .views import UserCreateView, UserDetailView, AddExpenseView, UserExpensesView, AllExpensesView, DownloadBalanceSheetView, login_view, home, logout_view, RegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home, name='home'),
    path('register', RegistrationView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('expenses/', AddExpenseView.as_view(), name='add-expense'),
    path('expenses/user/', UserExpensesView.as_view(), name='user-expenses'),
    path('expenses/all/', AllExpensesView.as_view(), name='all-expenses'),
    path('balance-sheet/', DownloadBalanceSheetView.as_view(), name='balance-sheet'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
