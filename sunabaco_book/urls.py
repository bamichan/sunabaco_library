from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sunabaco_book'


urlpatterns = [
    path('', views.index, name='index'),
    path('borrow/', views.borrow, name='borrow'),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)