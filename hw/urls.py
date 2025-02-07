from django.conf.urls.static import static    ## add for static files
from django.conf import settings
from django.urls import path

from hw import views

urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.home_page, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)