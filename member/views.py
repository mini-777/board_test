from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import json

from . import models


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
        return render(request, 'register.html')

    elif request.method == "POST":
        if request.POST.get('register') == '1':
            username = request.POST.get('username', None)
            # print(username)
            password = request.POST.get('password', None)
            # print(password)
            re_password = request.POST.get('re_password', None)
            # print(re_password)
            email = request.POST.get('email', None)
            phoneNum = request.POST.get('phoneNum', None)
            addrPost = request.POST.get('sample6_postcode', None)
            addrMain = request.POST.get('sample6_address', None)
            addrExtra = request.POST.get('sample6_extraAddress', None)
            addrDetail = request.POST.get('sample6_detailAddress', None)
            addr = addrMain + addrPost + addrExtra + addrDetail

            res_data = {}
            print( not(request.POST.get('agree1') and request.POST.get('agree2')))
            if not (username and password and re_password and email and phoneNum):
                print('모든 값을 입력하세요!')
            elif not request.session.get('phoneAuth'):
                print('휴대폰 인증을 받으세요!')
            elif password != re_password:
                print('비밀번호가 다릅니다')
            elif not (request.POST.get('agree1') and request.POST.get('agree2')):
                print('약관에 모두 동의해주세요')
            else:
                context = {'message': 'success'}
                member = models.BoardMember(
                    username=username,
                    email=email,
                    password=make_password(password),
                    phone_num=phoneNum,
                    address=addr,
                )
                member.save()
                return HttpResponse(json.dumps(context), content_type="application/json")
            return render(request, 'register.html', res_data)
        elif request.POST.get('authRegister') == '1':
            try:
                p_num = request.POST.get('phoneNum', None)
            except KeyError:
                message = '제대로 입력하세요!'
            else:
                models.auth_phone.objects.update_or_create(phone_number=p_num)
                message = '인증번호가 전송되었습니다'
            context = {'message': message}
            return HttpResponse(json.dumps(context), content_type="application/json")
        elif request.POST.get('auth') == '1':
            try:
                p_num = request.POST.get('phoneNum', None)
                a_num = request.POST.get('authNum', None)
            except KeyError:
                message = '제대로 입력하세요!'
            else:
                result = models.auth_phone.check_auth_number(p_num, a_num)
                print(result)
                if result:
                    message = '인증에 성공하였습니다 !'
                    request.session['phoneAuth'] = p_num
                else:
                    message = "인증에 실패하였습니다"
            context = {'message': message}
            return HttpResponse(json.dumps(context), content_type="application/json")

        # return render(request, 'register.html')
