from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt


from .models import User, Book, UserManager
def index(request):
    return render(request, "main/index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(hash1)
        newuser = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash1)
        request.session['id'] = newuser.id
        return redirect('/main/' + str(newuser.id))

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        request.session['id'] = User.objects.get(email=request.POST["email"]).id
        return redirect('/main/' + str(request.session['id']))

def logout(request):
    request.session.clear()
    return redirect('/')

def user_page(request, num):
    print(request.session['id'], num)
    if ('id' in request.session) and (request.session['id'] == int(num)):
        context = {
            "ID": num,
            "Name": User.objects.get(id=num).first_name,
            "Books": Book.objects.all(),
            "Faves": User.objects.get(id=num).fave_books.all()
        }
        return render(request, "main/main.html", context)
    else:
        print(request.session['id'] == num)
        return redirect('/')

def addbook(request):
    if request.method == "POST":
        errors = User.objects.add_book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/main/' + str(request.session['id']))
        else:
            newBook = Book.objects.create(title = request.POST['title'], description = request.POST['description'], uploaded_by = User.objects.get(id=request.session['id']))
            newBook.fave_users.add(User.objects.get(id=request.session['id']))
            return redirect('/main/' + str(request.session['id']))
    else:
        return redirect('/main/' + str(request.session['id']))

def book_page(request, num):
    if ('id' in request.session):
        context = {
            "User": User.objects.get(id = request.session['id']),
            "Name": User.objects.get(id=request.session['id']).first_name,
            "ID": num,
            "Title": Book.objects.get(id=num).title,
            "Description": Book.objects.get(id=num).description,
            "Added": Book.objects.get(id=num).uploaded_by,
            "Dates": Book.objects.get(id=num),
            "Faves": Book.objects.get(id=num).fave_users.all()
        }
        return render(request, "main/book.html", context)
    else:
        return redirect('/')

def add_favorite(request, num):
    if ('id' in request.session):
        fave_book = Book.objects.get(id=num)
        fave_book.fave_users.add(User.objects.get(id=request.session['id']))
        return redirect(f'/book/{num}')
    else:
        return redirect('/')

def unfavorite(request, num):
    if ('id' in request.session):
        fave_book = Book.objects.get(id=num)
        fave_book.fave_users.remove(User.objects.get(id=request.session['id']))
        return redirect(f'/main/' + str(request.session['id']))
    else:
        return redirect('/')

def remove(request, num):
    if ('id' in request.session):
        rem_book = Book.objects.get(id=num)
        rem_book.delete()
        return redirect(f'/main/' + str(request.session['id']))
    else:
        return redirect('/')