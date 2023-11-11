from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomerRegistrationForm, MenuForm
from django.contrib.auth.models import Group
from django.shortcuts import render
from .models import Menu
from django.http import JsonResponse

class CustomerRegistrationView(View):
    def get(self, request):
        return render(request, "register.html", {"form":CustomerRegistrationForm})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to "customer" group
            customer_group = Group.objects.get(name='customer')
            user.groups.add(customer_group)
            # Log the User in 
            login(request, user)
            return redirect('orders')
        return render(request, "register.html", {"form":form})
    


# Add code for form_view() function below

def form_view(request):
    pass