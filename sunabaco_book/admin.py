from django.contrib import admin
from sunabaco_book.models import Bookimage, Reservation, Review
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
    list_display = ('id', 'title', 'genre', 'Author', 'body', 'image', 'lending', 'book_status', 'created_at')
    list_display_link = ('id', 'title', 'genre', 'Author', 'body', 'image', 'lending', 'book_status', 'created_at')
    search_fields = ('id', 'title', 'genre', 'Author', 'body', 'image', 'lending', 'book_status', 'created_at')
    actions = [make_pick1_up, make_pick2_up, make_pick3_up, make_pick4_up]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_image', 'lending_user_id', 'book_id', 'return_date', 'created_at')
    list_display_link = ('id', 'book_image', 'lending_user_id', 'book_id', 'return_date', 'created_at')
    search_fields = ('id', 'book_image', 'lending_user_id', 'book_id', 'return_date', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('point', 'body', 'target')
    list_display_link = ('point', 'body', 'target')
    search_fields = ('point', 'body', 'target')
