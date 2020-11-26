import requests
import time
import datetime
import json
import hashlib
import hmac
import base64
from .secretApi import sendMessage
from django.utils import timezone
from model_utils.models import TimeStampedModel
from random import randint
from django.db import models


# make models in here
class BoardMember(models.Model):
    username = models.CharField(max_length=100, verbose_name='유저ID')
    email = models.EmailField(max_length=100, verbose_name='유저메일')
    password = models.CharField(max_length=100, verbose_name='유저PW')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='마지막수정일')
    phone_num = models.CharField(verbose_name='휴대폰 번호', max_length=11)
    address = models.CharField(verbose_name="주소", max_length=200)
    carNum = models.CharField(verbose_name='차량번호', max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'boardmembers'
        verbose_name = '게시판멤버'
        verbose_name_plural = '게시판멤버'


class auth_phone(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'auth'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_sms()  # 인증번호가 담긴 SMS를 전송

    def send_sms(self):
        body = {
            "type": "SMS",
            "contentType": "COMM",
            "countryCode": "82",
            "from": "01028290575",
            "content": "[테스트] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number),
            "messages": [
                {
                    "to": self.phone_number
                }
            ]

        }
        body2 = json.dumps(body)
        url, headers = sendMessage()
        requests.post(url, headers=headers, data=body2)

    @classmethod
    def check_auth_number(cls, p_num, c_num):
        time_limit = timezone.now() - datetime.timedelta(minutes=5)
        result = cls.objects.filter(
            phone_number=p_num,
            auth_number=c_num,
            modified__gte=time_limit
        )
        if result:
            return True
        return False
