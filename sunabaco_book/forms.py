from django import forms
from sunabaco_book.models import Bookimage, Reservation
from django import forms


class BookimageCreateForm(forms.ModelForm):

    class Meta:
        model = Bookimage
        fields = ['title', 'genre', 'Author', 'body', 'image']
        
        

class ReservationCreateForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = ['return_date']
        # widgets = {
        #         'return_date': DatePickerInput(
        #             format='%Y-%m-%d',
        #             attrs={'readonly': 'true'},
        #             options={
        #                 'locale': 'ja',
        #                 'dayViewHeaderFormat': 'YYYY年 MMMM',
        #                 'ignoreReadonly': True,
        #                 'allowInputToggle': True,
        #             }
        #     )
        # }

class Return_bookForm(forms.ModelForm):

    class Meta:
        model = Bookimage
        fields = ['book_status']
        widgets = {
            'book_status': forms.HiddenInput,
        }
