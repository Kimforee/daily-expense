# expenses/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, mobile_number, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile_number, password=None):
        user = self.create_user(email, name, mobile_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_number']

    def __str__(self):
        return self.email

class Expense(models.Model):
    SPLIT_METHOD_CHOICES = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    ]
    
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHOD_CHOICES)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses_created')
    participants = models.ManyToManyField(CustomUser, through='ExpenseSplit', related_name='participating_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class ExpenseSplit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.name} owes {self.amount_owed} for {self.expense.description}"