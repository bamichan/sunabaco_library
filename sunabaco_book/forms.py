from django import forms
<<<<<<< HEAD
from sunabaco_book.models import Bookimage, Reservation
from django import forms
from bootstrap_datepicker_plus import DatePickerInput


class ReservationCreateForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = ['return_date', 'isbn']
        widgets = {
                'return_date': DatePickerInput(
                    format='%Y-%m-%d',
                    options={
                        'locale': 'ja',
                        'dayViewHeaderFormat': 'YYYY年 MMMM',
                    }
            )
        }
=======
from django.contrib.auth import forms as auth_forms

class LoginForm(auth_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'

>>>>>>> origin/master
