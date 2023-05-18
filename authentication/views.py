from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error("User name  already exit , try again please")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error("Email already exit")

        if len(username) > 10:
            messages.error("username should be more that 10 char")
        if pass1 != pass2:
            messages.error("Password isn't matching , enter same pwd")
        if username.isalnum():
            messages.error("username shouldn't be alpha numeric char")
            return redirect('home')


        my_user = User.objects.create_user(username, email, pass1)
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.save()

        messages.success(request, "your account has been success full created")
        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        pass1 = request.POST.get('pass1', '')

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {"fname": fname})

        else:
            messages.error(request, "Bad credentials")
            return redirect('home')
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logout successfully..!")
    return redirect('home')
