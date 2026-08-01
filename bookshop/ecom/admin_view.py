from django.shortcuts import redirect, render
from .models import Genre, Book
from django.contrib.auth.decorators import login_required


@login_required
def admin_dashboard(req):
    data = {
        "genre" : Genre.objects.count(),
        "books" : Book.objects.count(),
    }
    return render(req, "admin/dashboard.html",data)


@login_required
def insert_genre(req):
    if req.method == "POST":
        g = Genre()
        g.title = req.POST.get("title")
        g.description = req.POST.get("description")
        g.save()
        return redirect(insert_genre)

    return render(req, "admin/insert_genre.html")


@login_required
def insert_book(req):
    data = {
        "genre" : Genre.objects.all()
    }
    if req.method == "POST":
        b = Book()
        b.title = req.POST.get("title")
        b.author = req.POST.get("author")
        b.nop = req.POST.get("nop")
        b.isbn = req.POST.get("isbn")
        b.publish_year = req.POST.get("publish_year")
        b.genre = Genre.objects.get(id=req.POST.get("genre"))
        b.cover_image = req.FILES.get("cover_image")
        b.save()
        return redirect(insert_book)

    return render(req, "admin/insert_book.html",data)


@login_required
def manage_genre(req):
    data = {
        "genre" : Genre.objects.all()
    }
    return render(req, "admin/manage_genre.html",data)


@login_required
def manage_books(req):
    data = {
        "books" : Book.objects.all()
    }
    return render(req, "admin/manage_books.html",data)

@login_required
def delete_genre(req,id):
    data = {}
    try:
        g = Genre.objects.get(id=id)
        g.delete()
        return redirect(manage_genre)
    except Genre.DoesNotExist:
        data['error'] = "Not Found"

    return redirect(manage_genre)
    
@login_required
def delete_book(req,id):
    data = {}
    try:
        b = Book.objects.get(id=id)
        b.delete()
        return redirect(manage_books)
    except Genre.DoesNotExist:
        data['error'] = "Not Found"

    return redirect(manage_books)

@login_required
def edit_book(req, id):
    book = Book.objects.get(id=id)
    
    if req.method == "POST":
        book.title = req.POST.get("title")
        book.author = req.POST.get("author")
        book.nop = req.POST.get("nop")
        book.isbn = req.POST.get("isbn")
        book.publish_year = req.POST.get("publish_year")
        book.genre = Genre.objects.get(id=req.POST.get("genre"))
        book.cover_image = req.FILES.get("cover_image")
        book.save()
        return redirect(insert_book)
    return render(req, "admin/insert_book.html",{"book":book})

    
@login_required
def edit_genre(req, id):
    genre = Genre.objects.get(id=id)
    if req.method == "POST":
        genre.title = req.POST.get("title")
        genre.description = req.POST.get("description")
        genre.save()
        return redirect(insert_genre)
    return render(req, "admin/insert_genre.html",{"genre":genre})

    