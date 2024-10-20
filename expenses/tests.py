from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Expense, ExpenseSplit

class ExpenseTests(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email="user1@example.com", password="pass123", name="User One", mobile_number="1234567890")
        self.user2 = CustomUser.objects.create_user(email="user2@example.com", password="pass123", name="User Two", mobile_number="0987654321")
        self.user3 = CustomUser.objects.create_user(email="user3@example.com", password="pass123", name="User Three", mobile_number="5678901234")
        self.client.login(email='user1@example.com', password='pass123')

    def test_create_user(self):
        """
        Test user creation with the required fields.
        """
        url = reverse('user-create')
        data = {'email': 'newuser@example.com', 'password': 'newpassword', 'name': 'New User', 'mobile_number': '0123456789'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_expense_equal_split(self):
        """
        Test adding an expense with equal split among users.
        """
        url = reverse('add-expense')
        data = {
            "description": "Lunch",
            "amount": 100.0,
            "split_method": "equal",
            "creator": 1,
            "participants": [1, 2]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)

        # Check if ExpenseSplit was created correctly
        expense = Expense.objects.first()
        splits = ExpenseSplit.objects.filter(expense=expense)
        self.assertEqual(splits.count(), 2)

        # Verify the split amounts are correct (for equal split)
        for split in splits:
            self.assertEqual(split.amount_owed, 50.0)

    def test_add_expense_exact_split(self):
        """
        Test adding an expense with exact split amounts.
        """
        url = reverse('add-expense')
        data = {
            "description": "Dinner",
            "amount": 100.0,
            "split_method": "exact",
            "creator": 1,  # Assuming creator ID is 1
            "splits": [
                {"user": 1, "amount_owed": 40.0},
                {"user": 2, "amount_owed": 60.0}
            ],
            "participants": [1, 2]  # Assuming participant IDs are 1 and 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)

        # Check if ExpenseSplit was created correctly
        expense = Expense.objects.first()
        splits = ExpenseSplit.objects.filter(expense=expense)
        self.assertEqual(splits.count(), 2)

        # Verify the exact split amounts are correct
        self.assertEqual(splits[0].amount_owed, 40.0)
        self.assertEqual(splits[1].amount_owed, 60.0)

    def test_add_expense_percentage_split(self):
        """
        Test adding an expense with percentage split.
        """
        url = reverse('add-expense')
        data = {
            "description": "Brunch",
            "amount": 100.0,
            "split_method": "percentage",
            "creator": 1,
            "amount_owed": [
                {"user": 1, "percentage": 40.0},
                {"user": 2, "percentage": 60.0}
            ],
            "participants": [1, 2]
        }
        response = self.client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)

    def test_user_expenses(self):
        """
        Test retrieving expenses for a specific user.
        """
        # Add an expense with user1 as a participant
        expense = Expense.objects.create(description="Lunch", amount=1000, split_method="equal", creator=self.user1)
        ExpenseSplit.objects.create(user=self.user1, expense=expense, amount_owed=500)
        ExpenseSplit.objects.create(user=self.user2, expense=expense, amount_owed=500)

        url = reverse('user-expenses')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_all_expenses(self):
        """
        Test retrieving all expenses.
        """
        # Add two expenses
        Expense.objects.create(description="Lunch", amount=1000, split_method="equal", creator=self.user1)
        Expense.objects.create(description="Groceries", amount=500, split_method="equal", creator=self.user2)

        url = reverse('all-expenses')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_download_balance_sheet(self):
        Expense.objects.create(description="Lunch", amount=1000, split_method="equal", creator=self.user1)
        
        url = reverse('balance-sheet')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="balance_sheet.csv"')

