from rest_framework import serializers
from .models import CustomUser, Expense, ExpenseSplit
from .utils import split_equal, split_exact, split_percentage
from .models import CustomUser 

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

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser(
            name=validated_data['name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class ExpenseSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ['user', 'amount_owed']

class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True, required=False)
    participants = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)

    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'split_method', 'creator', 'splits', 'participants']

    def create(self, validated_data):
        splits_data = validated_data.pop('splits', [])
        participants = validated_data.pop('participants', [])
        split_method = validated_data.get('split_method')

        # Create the expense instance
        expense = Expense.objects.create(**validated_data)

        # Split logic based on the split_method
        if split_method == 'equal':
            splits = split_equal(expense, participants)
        elif split_method == 'exact':
            splits = split_exact(expense, {split['user'].id: split['amount_owed'] for split in splits_data})
        elif split_method == 'percentage':
            splits = split_percentage(expense, {split['user'].id: split.get('percentage', 0) for split in splits_data})

        # Save each split
        for split in splits:
            # Check if `split` is a model instance and convert to dict if needed
            if isinstance(split, ExpenseSplit):
                split = {
                    'user': split.user,
                    'amount_owed': split.amount_owed
                }

            # Create ExpenseSplit objects with the expense reference
            ExpenseSplit.objects.create(expense=expense, **split)

        return expense
