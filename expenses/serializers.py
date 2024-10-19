# expenses/serializers.py
from rest_framework import serializers
from .models import CustomUser, Expense, ExpenseSplit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'mobile_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            mobile_number=validated_data['mobile_number'],
            password=validated_data['password']
        )
        return user

class ExpenseSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ['user', 'amount_owed']

class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True, write_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'split_method', 'creator', 'splits', 'participants']

    def create(self, validated_data):
        splits_data = validated_data.pop('splits')
        expense = Expense.objects.create(**validated_data)
        
        for split_data in splits_data:
            ExpenseSplit.objects.create(expense=expense, **split_data)
        
        return expense