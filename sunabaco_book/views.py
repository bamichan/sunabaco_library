from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from sunabaco_book.forms import LoginForm

from django.template.context_processors import media
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
# ------------------------------------------------------------------

class UserLoginView(LoginView):
    form_class = LoginForm

login = UserLoginView.as_view()

logout = LogoutView.as_view()



# Create your views here.
def index(request):

    return render(request,'sunabaco_book/books.html')

def borrow(request):

    return render(request,'sunabaco_book/borrow.html')
