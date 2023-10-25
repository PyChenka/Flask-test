import os

from flask import Flask


# инициализация фреймворка
app = Flask(__name__)

# рандомный secret key для сессии
app.config['SECRET_KEY'] = os.urandom(24)


# параметры подключения к БД
app.config['DATABASE'] = {
    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': '123',
    'HOST': 'localhost',
    'PORT': '5432',
    'OPTIONS': '-c search_path=flask'
}