from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sunabaco_book'


urlpatterns = [
    path('', views.index, name='index'),
    path('books_detail/<pk>/', views.book_detail, name='detail'),
    path('books/reservation_book/<pk>', views.reservation_book, name='reservation_book'),
    path('books/return_book/<pk>', views.return_book, name='return_book'),
    path('books_list/', views.book_list, name='list'),
    path('borrow/', views.borrow, name='borrow'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
