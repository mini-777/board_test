DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_board',
        'USER': 'admin',
        'PASSWORD': 'dkssudgktpdy',
        'HOST': 'database-1.cip9531xqh6o.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}