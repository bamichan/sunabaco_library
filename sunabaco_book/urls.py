from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sunabaco_book'


urlpatterns = [
    path('', views.index, name='index'),
    path('books/create/', views.book_create, name='create'),
    path('books_list/', views.book_list, name='list'),
    path('books_detail/<pk>/', views.book_detail, name='detail'),
    path('borrow/', views.borrow, name='borrow'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)