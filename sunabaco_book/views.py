import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from register.models import User 
from sunabaco_book.models import Bookimage, Reservation
from sunabaco_book.forms import ReservationCreateForm, Return_bookForm, BookimageCreateForm
from django.contrib.auth.views import LoginView, LogoutView
from django.template.context_processors import media
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Q
import requests
import os
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
import numpy as np



def index(request):
    return render(request, 'index.html')

# ------------------------------------------------------------------
class BookimageListView(generic.ListView):
    model = Bookimage
    template_name = 'sunabaco_book/bookimage_list.html'

    def post(self, request, *args, **kwargs):
        if request.POST['key_word']:
            key_word = request.POST['key_word']
            pattarn = "&title="
            key_word = pattarn+key_word
        elif request.POST['author']:
            author = request.POST['author']
            pattarn = "&author="
            key_word = pattarn+author
        else:
            messages.warning(self.request, '入力してください。')
            return redirect('sunabaco_book:list')

        RAKUTEN_APP_ID = 1058934488319555649
        REQUEST_URL = f"https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json{key_word}&booksGenreId=001004008&applicationId={RAKUTEN_APP_ID}"
        response = requests.get(REQUEST_URL)
        result = []
        result_book = response.json()["Items"]
        for book in result_book:
            result.append(book)
        return render(request, self.template_name, {'result': result})
    
    def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        if q_word:
            book_list = Bookimage.objects.filter(
                Q(title__icontains=q_word) | Q(Author__icontains=q_word))
        else:
            book_list = Bookimage.objects.all()
        return book_list

book_list = BookimageListView.as_view()

# ------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class BookimageDetailView(generic.DetailView):
    model = Bookimage

book_detail = BookimageDetailView.as_view()

# ------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class BookimageCreateView(generic.CreateView):
    model = Bookimage
    form_class = BookimageCreateForm

book_create = BookimageCreateView.as_view()

# ------------------------予約view--------------------------------------
@method_decorator(login_required, name='dispatch')
class ReservationCreate(generic.CreateView):
    template_name = 'sunabaco_book/reservation_form.html'
    model = Reservation
    form_class = ReservationCreateForm
    success_url = reverse_lazy('sunabaco_book:reservation_book')

    def form_valid(self, form, *args, **kwargs):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Bookimage, pk=post_pk)
        if post.book_status == 0:
            reservation = form.save(commit=False)
            post.book_status = 1
            post.save()
            reservation.book_id = post.id
            reservation.book_status = post.book_status
            reservation.book_image = post
            reservation.lending_user_id = self.request.user.id
            reservation.save()
            messages.success(self.request, 'レンタルのご予約は正常に送信されました。')
            return redirect('sunabaco_book:reservation_book', pk=post_pk)
        else:
            messages.warning(self.request, '現在貸し出し中です。')
            return redirect('sunabaco_book:reservation_book', pk=post_pk)

    def form_invalid(self, form):
        messages.warning(self.request, '入力値に誤りがあるようです、送信できませんでした。')
        return super().form_invalid(form)

reservation_book = ReservationCreate.as_view()

# ------------------------------返却-----------------------------------------
@method_decorator(login_required, name='dispatch')
class ReturnCreate(generic.CreateView):
    template_name = 'sunabaco_book/return_book.html'
    model = Bookimage
    form_class = Return_bookForm
    success_url = reverse_lazy('sunabaco_book:return_book')

    def form_valid(self, form, *args, **kwargs):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Bookimage, pk=post_pk)
        user = self.request.user.id
        rental_list = Reservation.objects.filter(lending_user_id=user, book_status=1)
        for rental in rental_list:
            if post.book_status == 1 and rental.book_status == 1:
                Reservation.objects.filter(book_id=post_pk).update(book_status=0)
                Bookimage.objects.filter(pk=post_pk).update(book_status=0)
                messages.success(self.request, 'ご返却ありがとうございます。')
                return redirect('sunabaco_book:return_book', pk=post_pk)
            else:
                messages.warning(self.request, 'こちらのアカウントではこの本は、借りていません。')
                return redirect('sunabaco_book:return_book', pk=post_pk)

    def form_invalid(self, form):
        messages.warning(self.request, '送信できませんでした。')
        return super().form_invalid(form)

return_book = ReturnCreate.as_view()


# ------------------------------マイページリスト--------------------------------------
@method_decorator(login_required, name='dispatch')
class MypageListView(generic.ListView):
    template_name = 'sunabaco_book/mypage_list.html'
    model = User
    

    def edit_contrast(self, image, gamma):
        look_up_table = [np.uint8(255.0 / (1 + np.exp(-gamma * (i - 128.) / 255.))) for i in range(256)]
        result_image = np.array([look_up_table[value] for value in image.flat], dtype=np.uint8)
        result_image = result_image.reshape(image.shape)
        return result_image

    cap = cv2.VideoCapture(0)
    
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    while cap.isOpened():
        ret,frame = cap.read()
        if ret == True:
            d = decode(frame)
            if d:
                for barcode in d:
                    x,y,w,h = barcode.rect
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                    barcodeData = barcode.data.decode('utf-8')
                    frame = cv2.putText(frame,barcodeData,(x,y-10),font,.5,(0,0,255),2,cv2.LINE_AA)
            cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history_list'] = Reservation.objects.filter(lending_user_id=self.request.user.id).all()
        return context

    def get_queryset(self):
        return User.objects.all()

mypage_list = MypageListView.as_view()
