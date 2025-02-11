from django.urls import path
from django.conf import settings
from django.conf.urls.static import static # Add for static files
from . import views

urlpatterns = [ 
    path(r'', views.home, name="home"),
    path(r'order', views.order, name="order"),
    path(r'submit', views.submit, name="submit"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)