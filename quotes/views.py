import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time

quotes = ["A book is just like life and anything can change.", "Today you are You, that is truer than true. There is no one alive who is Youer than You.", "Kid, you'll move mountains.", "It's not about what it is, it's about what it can become."]

images = ["https://cs-people.bu.edu/ktong22/QuoteImages/seuss1.jpg", "https://cs-people.bu.edu/ktong22/QuoteImages/seuss4.jpg", "https://cs-people.bu.edu/ktong22/QuoteImages/seuss3.jpg"] #upload to cspeoples website and make image directory and get link from that to here

def home_page(request):
    '''Define a view to show the 'home.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/home.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'quote':quotes[random.randint(0,2)],
        'image':images[random.randint(0,2)],
    }

    return render(request, template, context)

def quote(request):
    template = 'quotes/home.html'

    context = {
        'quote':quotes[random.randint(0,2)],
        'image':images[random.randint(0,2)],
    }

    return render(request, template, context)

def about(request):
    '''Define a view to show the 'about.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/about.html'

    return render(request, template)

def showAll(request):
    
    template = 'quotes/showall.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'quote1':quotes[0],
        'quote2':quotes[1],
        'quote3':quotes[2],
        'image1':images[0],
        'image2':images[1],
        'image3':images[2],
    }

    return render(request, template, context)
