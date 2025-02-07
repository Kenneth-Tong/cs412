from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.home_page, name="home"),
    path(r'about', views.about, name="about"), #go to the about section
    path(r'quote', views.quote, name="quote"), #generate new quotes
    path(r'showall', views.showAll, name="showall"), #show all the quotes and pictures
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
