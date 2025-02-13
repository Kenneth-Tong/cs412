import random
from django.shortcuts import render
from django.http import HttpRequest
import time

# Create your views here.

daily_special = [
    {"name": "Null Pointer Nachos", "description": "Loaded nachos with all the fixings.", "price": "8.99"},
    {"name": "Binary Tree Broccoli Salad", "description": "A fresh and healthy salad with a binary twist.", "price": "7.99"},
    {"name": "Cache Chocolate Cookie", "description": "A warm, gooey chocolate chip cookie.", "price": "3.99"},
    {"name": "Firewall Fries", "description": "Extra-crispy fries with a spicy dipping sauce.", "price": "4.99"},
    {"name": "Syntax Green Salad", "description": "A mix of fresh greens, fruits, and nuts.", "price": "6.99"},
    {"name": "Brunch Breakpoint", "description": "A build-your-own brunch plate with eggs, bacon, and toast.", "price": "12.99"},
    {"name": "Cloud Cupcake", "description": "A fluffy cupcake topped with whipped cream and sprinkles.", "price": "4.99"},
]

def home(request):
    '''Render the home page.'''
    template_name = "restaurant/main.html"

    return render(request, template_name)

def order(request):
    '''Show the web page with the order form.'''
    template_name = "restaurant/order.html"
    
    # Pass the daily special to the template
    choosen = random.randint(0, len(daily_special) - 1)

    context = {
        'daily_special': daily_special[choosen],
    }
    return render(request, template_name, context)

def submit(request: HttpRequest):
    '''Process the form submission and generate a confirmation.'''
    template_name = "restaurant/confirmation.html"

    cost = 0

    # Read the form data into Python variables
    if request.POST:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        instructions = request.POST.get('instructions')

        if instructions == "":
            instructions = "None"

        # Get selected toppings for Pizza Pi
        topping_number = 0
        toppings_list = ""

        if request.POST.getlist('toppings'):
            topping_number = len(request.POST.getlist('toppings'))
            for topping in request.POST.getlist('toppings'):
                if toppings_list == "": # Adding the first topping into the list
                    toppings_list = topping
                else:
                    toppings_list = toppings_list + ', ' + topping
        
        if len(toppings_list) == 0:
            toppings_list = "None" # There was no toppings selected

        # Get selected menu items
        selected_items = ""
        if request.POST.get('daily_special'):
            selected_items = selected_items + ', ' + request.POST.get('daily_special_name')
            cost += float(request.POST.get('daily_special_price'))
        if request.POST.get('byte_bagel'):
            selected_items = selected_items + ', ' + 'Byte-Sized Bagel'
            cost += 5.99
        if request.POST.get('linguine'):
            selected_items = selected_items + ', ' + 'Infinite Loop Linguine'
            cost += 12.99
        if request.POST.get('pizza'):
            selected_items = selected_items + ', ' +  'Pizza Pi (Toppings: ' + toppings_list + ')'
            cost += 10.99 + topping_number * 1.5

        if selected_items != "":
            selected_items = selected_items.replace(",", "", 1)

    # Get the current time for the order ready time
    current_time = time.localtime()
    random_delay = random.randint(30, 60)  # Random delay in seconds (30-60 minutes)
    ready_time = time.localtime(time.mktime(current_time) + random_delay * 60)
    ready_time_str = time.strftime('%I:%M %p', ready_time)

    # Prepare context for the confirmation page
    context = {
        'name': name,
        'phone': phone,
        'email': email,
        'instructions': instructions,
        'selected_items': selected_items,
        'toppings': toppings_list,
        'cost': cost,
        'readytime': ready_time_str,
    }

    return render(request, template_name, context)