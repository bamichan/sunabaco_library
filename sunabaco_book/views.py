import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from register.models import User 
from sunabaco_book.models import Bookimage, Reservation
from sunabaco_book.forms import ReservationCreateForm, Return_bookForm
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
def index(request):
    return render(request, 'index.html')

# ------------------------------------------------------------------
class BookimageListView(generic.ListView):
    model = Bookimage
    
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
        lending_user = Reservation.objects.get(pk=post_pk)

        if post.book_status == 1 and user == lending_user.lending_user_id:
            Bookimage.objects.filter(pk=post_pk).update(book_status=0)
            messages.success(self.request, 'ご返却ありがとうございます。')
            return redirect('sunabaco_book:return_book', pk=post_pk)
        else:
            messages.warning(self.request, 'このアカウントではこちらの本は、借りていません。')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history_list'] = Reservation.objects.filter(lending_user_id=self.request.user.id).all()
        return context

mypage_list = MypageListView.as_view()
