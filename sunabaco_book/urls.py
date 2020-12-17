from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'sunabaco_book'


urlpatterns = [
    path('', views.book_list, name='list'),
    path('create/', views.book_create, name='create'),
    path('accounts/profile/', views.index, name='index'),
    path('mypage/', views.mypage_list, name='mypage_list'),
    path('detail/<pk>/', views.book_detail, name='detail'),
    path('books/reservation_book/<pk>', views.reservation_book, name='reservation_book'),
    path('books/return_book/<pk>', views.return_book, name='return_book'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
