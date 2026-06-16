from django.shortcuts import render, redirect
from .models import User, Role
from django.contrib.auth.hashers import make_password, check_password

def login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)

            if check_password(password, user.password):

                request.session['user_id'] = user.id
                request.session['role'] = user.role.name
                request.session['username'] = user.username

                if user.role.name == 'Гость':
                    return redirect('wiki')

                return redirect("devices_home")

            else:
                return render(request, 'auth/login.html',{'error':'Неверный пароль!'})

        except User.DoesNotExist:
            return render (request,'auth/login.html', {'error': 'Пользователь не существует.'})

    return render(request,'auth/login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(request, "auth/register.html", {
                "error": "Пароли не совпадают",
            })

        if User.objects.filter(username=username).exists():
            return render(request, "auth/register.html", {
                "error": "Пользователь уже существует",
            })

        guest_role = Role.objects.get(name='Гость')

        User.objects.create(
            username=username,
            password=make_password(password),
            role=guest_role
        )

        return redirect("login")

    return render(request, "auth/register.html")