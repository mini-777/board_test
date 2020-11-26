from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .forms import LoginForm
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
        finally:
            pass
        return render(request, 'register.html')

    elif request.method == "POST":
        if request.POST.get('register') == '1':
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            re_password = request.POST.get('re_password', None)
            email = request.POST.get('email', None)
            phoneNum = request.POST.get('phoneNum', None)
            addrPost = request.POST.get('sample6_postcode', None)
            addrMain = request.POST.get('sample6_address', None)
            addrExtra = request.POST.get('sample6_extraAddress', None)
            addrDetail = request.POST.get('sample6_detailAddress', None)
            carNum = request.POST.get('carNum', None)
            addr = addrMain + addrPost + addrExtra + addrDetail
            message = 'success!'

            try:
                models.BoardMember.objects.get(username=username)
            except:
                pass
            else:
                message = '같은 username이 있습니다 다른 값을 입력하세요 !'

            try:
                models.BoardMember.objects.get(email=email)
            except:
                pass
            else:
                message = '같은 email이 있습니다 다른 값을 입력하세요 !'

            try:
                models.BoardMember.objects.get(carNum=carNum)
            except:
                pass
            else:
                message = '같은 차량번호가 있습니다 다른 값을 입력하세요 !'

            try:
                if request.session.get('phoneAuth').find(phoneNum) == -1:
                    message = '휴대폰 인증을 받으세요!'
            except:
                message = '휴대폰 인증을 받으세요!'

            if not (request.POST.get('agree1') == 'true' and request.POST.get('agree2') == 'true'):
                message = '약관에 모두 동의해주세요'
            elif not (username and password and re_password and email and addr and carNum):
                message = '모든 값을 입력하세요 !'
            elif email.find('@') == -1 and email.find('.') == -1:
                message = '이메일 양식을 확인해주세요'
            elif len(re.compile('[ |ㄱ-ㅎ|ㅏ-ㅣ]+').sub('', carNum)) <= 1 or len(carNum) < 7:
                message = '차량번호를 확인하세요 !'
            elif password != re_password:
                message = '비밀번호가 다릅니다'

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

            try:
                p_num = request.POST.get('phoneNum', None)
                phoneCheck = models.BoardMember.objects.get(phone_num=p_num)
            except:
                phoneCheck = None
            finally:
                if phoneCheck is None:
                    models.auth_phone.objects.update_or_create(phone_number=p_num)
                    message = '인증번호가 전송되었습니다'
                else:
                    message = '같은 전화번호가 있습니다 다른 값을 입력하세요 !'

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
                if result:
                    message = '인증에 성공하였습니다 !'
                    request.session['phoneAuth'] = p_num
                else:
                    message = "인증에 실패하였습니다"
            context = {'message': message}
            return HttpResponse(json.dumps(context), content_type="application/json")
