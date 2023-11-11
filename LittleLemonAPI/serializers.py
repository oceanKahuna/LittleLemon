from rest_framework import serializers
import bleach 
from .models import * 
from django.contrib.auth.models import Group

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem 
        fields = '__all__'

    def get_category_title(self,obj):
        return obj.category.title 

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart 
        fields = ['user','menuitem','quantity']
    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.groups.filter(name='Customer').exists():
            self.fields['user'].queryset = User.objects.filter(id=request.user.id)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username','first_name','last_name','groups']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group 
        fields = ['id','name']