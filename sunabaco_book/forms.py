from django import forms
from sunabaco_book.models import Bookimage, Reservation
from django import forms
from bootstrap_datepicker_plus import DatePickerInput


class ReservationCreateForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = ['return_date']
        widgets = {
                'return_date': DatePickerInput(
                    format='%Y-%m-%d',
                    attrs={'readonly': 'true'},
                    options={
                        'locale': 'ja',
                        'dayViewHeaderFormat': 'YYYY年 MMMM',
                        'ignoreReadonly': True,
                        'allowInputToggle': True,
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
