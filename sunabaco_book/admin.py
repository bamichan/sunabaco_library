from django.contrib import admin
from sunabaco_book.models import Bookimage, Reservation
from django.contrib import messages

# -------------------------------------------------------------------
def make_pick1_up(self, request, queryset):
    queryset.update(lending=0)
make_pick1_up.short_description = 'レンタルOK'

def make_pick2_up(self, request, queryset):
    queryset.update(lending=1)
make_pick2_up.short_description = '譲渡可能'

def make_pick3_up(self, request, queryset):
    queryset.update(lending=2)
make_pick3_up.short_description = '貸し出し不可'

def make_pick4_up(self, request, queryset):
    queryset.update(lending=3)
make_pick3_up.short_description = 'その他'

# -------------------------------------------------------------------
@admin.register(Bookimage)
class BookimageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn', 'genre', 'Author', 'body', 'image', 'lending', 'created_at')
    list_display_link = ('id', 'title', 'isbn', 'genre', 'Author', 'body', 'image', 'lending', 'created_at')
    search_fields = ('id', 'title', 'isbn', 'genre', 'Author', 'body', 'image', 'lending', 'created_at')
    actions = [make_pick1_up, make_pick2_up, make_pick3_up, make_pick4_up]

# @admin.register(Reservation)
# class ReservationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'start', 'end', 'book',)
#     list_display_link = ('id', 'user', 'start', 'end', 'book')
#     search_fields = ('id', 'user', 'start', 'end', 'book')
