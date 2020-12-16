from django import forms
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

class Return_bookForm(forms.ModelForm):

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

class Return_bookForm(forms.ModelForm):

    class Meta:
        model = Bookimage
        fields = ['book_status']
        widgets = {
            'book_status': forms.HiddenInput,
        }
