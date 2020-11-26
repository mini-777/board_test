from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from . import forms
from django.views.decorators.csrf import csrf_exempt
from . import models
import json
import re


def home(request):
    return render(request, 'home.html')


def agree(request):
    return render(request, 'agree.html')


def login(request):
    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            # session_code 검증하기
            request.session['user'] = form.user_id
            models.BoardMember.objects.update_or_create(id=form.user_id)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if request.session.get('user'):
        del (request.session['user'])
    return redirect('/')


@csrf_exempt
def register(request):
    if request.method == "GET":
        try:
            del (request.session['phoneAuth'])
        except:
            pass
        return render(request, 'register.html')

    elif request.method == "POST":
        if request.POST.get('register') == '1':
            form = RegisterForm(request.POST)
            message = form.errorCheck()

            if message == 'success!':  # form 에 입력된 정보들 DB에 입력
                member = models.BoardMember(
                    username=username,
                    email=email,
                    password=make_password(password),
                    phone_num=phoneNum,
                    address=addr,
                    carNum=carNum
                )
                member.save()

            context = {'message': message}
            return HttpResponse(json.dumps(context), content_type="application/json")
            return render(request, 'register.html')

        elif request.POST.get('authRegister') == '1':
            context = authRegister(request)
            return HttpResponse(json.dumps(context), content_type="application/json")

        elif request.POST.get('auth') == '1':
            context = auth(request)
            return HttpResponse(json.dumps(context), content_type="application/json")
