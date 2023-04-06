# -*- coding: utf-8 -*-
from django_exercise import sinaweibopy3

APP_KEY = '3278595304'
APP_SECRET = 'ec7364d69dd5e6a51498f9583fbf0074'
REDIRECT_URL = 'http://43.142.158.92:8081/girls/auth'

weibo_client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
