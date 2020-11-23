import sys
import os
import hashlib
import hmac
import base64
import requests
import time, json

def make_signature():
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    access_key = "pjTOluzDrm3CI7YANxyK"                # access key id (from portal or sub account)
    secret_key = "gBNN6AfYH8l4XclFt1n1iAKt8dpUbhru9Tcu881F"                # secret key (from portal or sub account)
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"
    uri = "/sms/v2/services/ncp:sms:kr:261726169955:board_test/messages"

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

def send_sms():
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    url = 'https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:261726169955:board_test/messages'
    body = {
        "type": "SMS",
        "contentType": "COMM",
        "countryCode": "82",
        "from": "01028290575",
        "content": "테스트",
        "messages": [
            {
                "to": "01028290575"
            }
        ]
       
    }
     # "to": [self.phone_number],
        # "content": "[테스트] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number)
    
    body2 = json.dumps(body)
    headers = {
        "Content-Type": 'application/json; charset=utf-8',
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": 'pjTOluzDrm3CI7YANxyK',
        "x-ncp-apigw-signature-v2": make_signature(),
    }
    res = requests.post(url, headers=headers, data=body2)
    print(res.json())
send_sms()