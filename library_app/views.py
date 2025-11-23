from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Users,Books,BookBorrowings
from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Q
from django.utils import timezone
from datetime import date,datetime,timedelta


# Create your views here.
def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_page(request):
    if request.method == 'POST':
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        try:
            user=Users.objects.get(username=username)
        except:
            messages.error(request,"Username is not valid")
            return redirect('/login')
        # if user.password_hash==password:                # if not password hash
        if check_password(password,user.password_hash):
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            return redirect("/book_list")
        else:
            messages.error(request,'Password is not valid')
            return redirect('/login')
    return render(request,'login.html')

def register_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        full_name = data.get("full_name")
        role = data.get("role")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Check if username already exists
        if Users.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("/register")

        # Check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("/register")

        # Create new user with hashed password
        user = Users.objects.create(
            username=username,
            full_name=full_name,
            role=role,
            password_hash=make_password(password),  # store hash
            is_active=True
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("/login")

    return render(request, "register.html")

def logout_page(request):
    request.session.flush()
    messages.success(request, "Logged out")
    return redirect('/login/')

def home(request):
    return redirect('/book_list')

@custom_login_required
def book_list(request):
    search_querry=request.GET.get('search')
    books=Books.objects.all()
    if search_querry :
        books=books.filter(
            Q(title__icontains=search_querry) | Q(author__icontains=search_querry)
        )
    return render(request,'book_list.html',{'books':books})

@custom_login_required
def add_book(request):
    if request.method == 'POST':
        data=request.POST
        title=data.get('title')
        author=data.get('author')
        isbn=data.get('isbn')
        genre=data.get('genre')
        total_copies=data.get('total_copies')
        pages=data.get('pages')
        available_copies=data.get('availabe_copies')
        description=data.get('description')

        user = Users.objects.get(id=request.session['user_id'])

        Books.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            total_copies=total_copies,
            pages=pages,
            available_copies=available_copies,
            description=description,
            created_by=user
        )

        return redirect("/book_list")
    return render(request,'add_book.html')

@custom_login_required
def edit_book(request,id):
    book=Books.objects.get(id=id)
    if request.method == 'POST':
        data=request.POST
        book.title=data.get('title')
        book.author=data.get('author')
        book.isbn=data.get('isbn')
        book.genre=data.get('genre')
        book.total_copies=data.get('total_copies')
        book.pages=data.get('pages')
        book.available_copies=data.get('available_copies')
        book.description=data.get('description')

        user = Users.objects.get(id=request.session['user_id'])

        book.created_by=user

        book.save()
        
        return redirect("/book_list")
    return render(request,'edit_book.html',{'book':book})

@custom_login_required
def delete_book(request,id):
    book=Books.objects.get(id=id)
    book.delete()
    return redirect('/book_list')

@custom_login_required
def borrow_book(request,id):
    book=Books.objects.get(id=id)
    available=book.available_copies
    if available > 0 :
        available-=1
        book.available_copies=available
        book.save()
        user= Users.objects.get(id=request.session['user_id'])
        current_date=timezone.now().date()
        BookBorrowings.objects.create(
            book=book,
            user=user,
            due_date=current_date+timedelta(days=14),
            is_returned=0,
        )
    else:
        messages.error("Can't borrow book , book is not availabe")
    return redirect('/book_list')

@custom_login_required
def dashboard(request):
    context={
        'books' : Books.objects.all(),
        'current_borrow_books' : BookBorrowings.objects.filter(is_returned=0),
        'available_books_count' : Books.objects.filter(available_copies__gt=0).count(),
        'overdue_books_count': BookBorrowings.objects.filter(due_date__lt=date.today(),is_returned=0).count(),
        'borrowing_history': BookBorrowings.objects.filter(is_returned=1),
        'today' : date.today(),
    }
    return render(request,'dashboard.html',context)

@custom_login_required
def return_book(request,id):
    book=BookBorrowings.objects.get(id=id)
    book_id=book.book.id

    book.returned_at=datetime.now()
    book.is_returned=1
    book.save()

    update_available_copies=Books.objects.get(id=book_id)
    update_available_copies.available_copies+=1
    update_available_copies.save()

    return redirect('/book_list')
