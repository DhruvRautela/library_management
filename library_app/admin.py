from django.contrib import admin
from .models import Users, Books, BookBorrowings, UserSessions

class BooksAdmin(admin.ModelAdmin):
    list_display=["title","author"]

class UsersAdmin(admin.ModelAdmin):
    list_display=["full_name","role"]

class BookBorrowingsAdmin(admin.ModelAdmin):
    list_display = ["get_book_title", "get_username", "borrowed_at"]

    def get_book_title(self, obj):
        return obj.book.title
    get_book_title.admin_order_field = "book"   # allows column sorting
    get_book_title.short_description = "Book Title"

    def get_username(self, obj):
        return obj.user.full_name
    get_username.admin_order_field = "user"
    get_username.short_description = "User"

class UserSessionsAdmin(admin.ModelAdmin):
    list_display=["user"]

admin.site.register(Users,UsersAdmin)
admin.site.register(Books,BooksAdmin)
admin.site.register(BookBorrowings,BookBorrowingsAdmin)
admin.site.register(UserSessions,UserSessionsAdmin)
