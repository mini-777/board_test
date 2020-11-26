from django.contrib.auth.hashers import check_password
from django import forms
from .models import BoardMember
from . import models
import re


class LoginForm(forms.Form):
    # 입력받을 값 두개
    username = forms.CharField(error_messages={
        'required': '아이디를 입력하세요!'
    }, max_length=100, label="사용자이름")
    password = forms.CharField(error_messages={
        'required': '비밀번호를 입력하세요!'
    }, widget=forms.PasswordInput, max_length=100, label="비밀번호")

    # 처음 값이 들어왔다 는 검증 진행

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                member = BoardMember.objects.get(username=username)
            except BoardMember.DoesNotExist:
                self.add_error('username', '아이디가 없습니다!')
                return
                # 예외처리를 하고 return 을 실행해서 바로 아래 코드를 실행하지 않고 빠져나오게 한다.
            if not check_password(password, member.password):
                self.add_error('password', '비밀번호가 다릅니다!')
            else:
                self.user_id = member.id


class RegisterForm:

    def __init__(self, request):
        # request 에서 input 값 받아오기
        self.username = request.POST.get('username', None)
        self.password = request.POST.get('password', None)
        self.rePassword = request.POST.get('re_password', None)
        self.email = request.POST.get('email', None)
        self.phoneNum = request.POST.get('phoneNum', None)
        self.addrPost = request.POST.get('sample6_postcode', None)
        self.addrMain = request.POST.get('sample6_address', None)
        self.addrExtra = request.POST.get('sample6_extraAddress', None)
        self.addrDetail = request.POST.get('sample6_detailAddress', None)
        self.carNum = request.POST.get('carNum', None)
        self.address = addrMain + addrPost + addrExtra + addrDetail

    def errorCheck(self):
        message = 'success!'
        if BoardMember.objects.filter(username=self.username).exists():
            message = '같은 username이 있습니다 다른 값을 입력하세요 !'
        elif BoardMember.objects.filter(email=self.email).exists():
            message = '같은 email이 있습니다 다른 값을 입력하세요 !'
        elif BoardMember.objects.filter(carNum=self.carNum).exists():
            message = '같은 차량번호가 있습니다 다른 값을 입력하세요 !'
        if not request.session.get('phoneAuth'):
            message = '휴대폰 인증을 받으세요!'
        if not (request.POST.get('agree1') == 'true' and request.POST.get('agree2') == 'true'):
            message = '약관에 모두 동의해주세요'
        elif not (self.username and self.password and self.re_password and self.email and self.addr and self.carNum):
            message = '모든 값을 입력하세요 !'
        elif email.find('@') == -1 and email.find('.') == -1:
            message = '이메일 양식을 확인해주세요'
        elif len(re.compile('[ |ㄱ-ㅎ|ㅏ-ㅣ]+').sub('', self.carNum)) <= 1 or len(self.carNum) < 7:
            message = '차량번호를 확인하세요 !'
        elif self.password != self.re_password:
            message = '비밀번호가 다릅니다'

        return message


def authRegister(request):
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

    return {'message': message}


def auth(request):
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
    return {'message': message}
