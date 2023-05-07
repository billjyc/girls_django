# -*- coding: utf-8 -*-
from django_exercise import sinaweibopy3

APP_KEY = '3278595304'
APP_SECRET = 'ec7364d69dd5e6a51498f9583fbf0074'
REDIRECT_URL = 'http://192.168.31.172:8000/snh48/weibo/get_code'

weibo_client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
