from django.urls import path
from .views import login_page,book_list,logout_page,add_book,edit_book,delete_book,borrow_book,dashboard,home,register_page,return_book

urlpatterns = [
    path('',home,name='home'),
    path('book_list/',book_list,name="book_list"),
    path('register/',register_page,name='register'),
    path('login/',login_page,name='login'),
    path('logout/',logout_page,name='logout'),
    path('add_book/',add_book,name='add_book'),
    path('edit_book/<int:id>/',edit_book,name='edit_book'),
    path('delete_book/<int:id>/',delete_book,name="delete_book"),
    path('borrow_book/<int:id>/',borrow_book,name='borrow_book'),
    path('dashboard/',dashboard,name='dashboard'),
    path('return_book/<int:id>/',return_book,name='return_book'),
]
