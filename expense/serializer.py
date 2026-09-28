from rest_framework import serializers
from expense.models import Expenses
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def create(self,validate_data):
        return User.objects.create_user(**self.validated_data)

class ExpenseSerializer(serializers.ModelSerializer):

    # owner=serializers.StringRelatedField(read_only=True)
    owner=serializers.SerializerMethodField()
    class Meta:
        model=Expenses
        fields = ['id', 'title', 'category', 'amount', 'created_at', 'owner']
        read_only_fields=['id','created_at','owner']

    def get_owner(self,obj):
        return obj.owner.username