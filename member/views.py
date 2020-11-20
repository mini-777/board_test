from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm

from .models import BoardMember


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # session_code 검증하기
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    if request.session.get('user'):
        del (request.session['user'])

    return redirect('/')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        # print (request.POST)
        username = request.POST.get('username', None)
        # print(username)
        password = request.POST.get('password', None)
        # print(password)
        re_password = request.POST.get('re_password', None)
        # print(re_password)
        email = request.POST.get('email', None)

        res_data = {}
        if not (username and password and re_password and email):
            res_data['error'] = '모든 값을 입력하세요!'

        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다'
            print(res_data)

        else:
            member = BoardMember(
                username=username,
                email=email,
                password=make_password(password)
            )
            member.save()
            return redirect('/member/login')

        return render(request, 'register.html', res_data)

