<<<<<<< HEAD
import datetime
=======
>>>>>>> origin/master
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from register.models import User 
from sunabaco_book.models import Bookimage, Reservation 
from sunabaco_book.forms import ReservationCreateForm
=======
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from sunabaco_book.forms import LoginForm

>>>>>>> origin/master
from django.template.context_processors import media
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
# ------------------------------------------------------------------

<<<<<<< HEAD
=======
class UserLoginView(LoginView):
    form_class = LoginForm

login = UserLoginView.as_view()

logout = LogoutView.as_view()

>>>>>>> origin/master


# Create your views here.
def index(request):

    return render(request,'sunabaco_book/books.html')

def borrow(request):

    return render(request,'sunabaco_book/borrow.html')
<<<<<<< HEAD


class BookimageListView(generic.ListView):
    model = Bookimage
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['sunabaco_list'] = Bookimage.objects.all()
    #     return context

    # def get_queryset(self):
    #     return Bookimage.objects.all()

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
        reservation = form.save(commit=False)
        reservation.user_id = self.request.user.id
        reservation.save()
        messages.success(self.request, 'レンタルのご予約は正常に送信されました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '送信できませんでした。')
        return super().form_invalid(form)

reservation_book = ReservationCreate.as_view()


def get_queryset(self, request, queryset):
        self.request.Bookimage.objects.filter(isbn=self).update(book_status=1)

=======
>>>>>>> origin/master
