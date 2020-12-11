from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from sunabaco_book.forms import LoginForm
from sunabaco_book.models import Bookimage 

from django.template.context_processors import media
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
# ------------------------------------------------------------------



# Create your views here.
def index(request):

    return render(request,'sunabaco_book/books.html')

def borrow(request):

    return render(request,'sunabaco_book/borrow.html')


class BookimageListView(generic.ListView):
    model = Bookimage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = profile.objects.all()
        return context

    def get_queryset(self):
        return Bookimage.objects.all()

bookimage_list = BookimageListView.as_view()

# ------------------------------------------------------------------
class BookimageDetailView(generic.DetailView):
    model = Bookimage

bookimage_detail = BookimageDetailView.as_view()


