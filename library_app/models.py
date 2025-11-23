from django.db import models

class BookBorrowings(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey('Books', models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(blank=True, null=True)
    is_returned = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_borrowings'


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(unique=True, max_length=13, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, default='English', blank=True)
    description = models.TextField(blank=True, null=True)
    cover_image_url = models.CharField(max_length=500, blank=True, null=True)
    available_copies = models.IntegerField(default=1, blank=True, null=True)
    total_copies = models.IntegerField(default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'Users',
        models.RESTRICT,
        db_column='created_by',
        related_name='book_created'
    )

    class Meta:
        managed = False
        db_table = 'books'


class UserSessions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey('Users', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_sessions'


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=10,
        choices=(('admin','Admin'),('librarian','Librarian'),('user','User')),
        default='user'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'users'
