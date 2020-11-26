import requests
import time
import datetime
import json
import hashlib
import hmac
import base64
from . import secretApi
from django.utils import timezone
from model_utils.models import TimeStampedModel
from random import randint
from django.db import models


def sendMessage():
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    access_key = "pjTOluzDrm3CI7YANxyK"  # access key id (from portal or sub account)
    secret_key = "gBNN6AfYH8l4XclFt1n1iAKt8dpUbhru9Tcu881F"  # secret key (from portal or sub account)
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"
    uri = "/sms/v2/services/ncp:sms:kr:261726169955:board_test/messages"

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    url = 'https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:261726169955:board_test/messages'

    headers = {
        "Content-Type": 'application/json; charset=utf-8',
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": 'pjTOluzDrm3CI7YANxyK',
        "x-ncp-apigw-signature-v2": signingKey,
    }
    return url, headers
