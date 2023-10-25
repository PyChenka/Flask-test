from flask import render_template, url_for, request, flash, session, redirect, abort, g

from FDataBase import FDataBase
from services_db import *


# представление для адреса
@app.route('/')
def index():
    database = open_db_connection()
    db = FDataBase(database)
    return render_template('index.html', menu=db.get_menu())


# можно два адреса обрабатывать одним представлением
@app.route('/new_page')
@app.route('/new')
def new():
    print(url_for('new')) # получает URL из функции-обработчика
    return render_template('new.html', site="Хомячки PRO") # переменная контекста


# динамические адреса
# path - несколько /../..
# int - только цифры
@app.route('/user/<int:username>/<path>')
def user(username, path):
    return f'Пользователь: {username}, адрес: {path}'


# обработчик после авторизации
@app.route('/profile/<user>')
def profile(user):
    if 'userLogged' not in session or session['userLogged'] != user:
        abort(401)
    return f'Пользователь: {user}'


# обработчик формы
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['message']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Введите сообщение')
    return render_template('form.html')


# декоратор для обработки ошибок
@app.errorhandler(404)
def page_not_found(error):
    # можно тута добавить ссылку на главную
    # указать 404 - вернется эта ошибка, а не 200 по дефолту
    return 'Кастомный шаблон для ошибки 404 должен быть здесь', 404


@app.errorhandler(401)
def page_not_found(error):
    return '<h1>Ошибка доступа</h1>', 401


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', user=session['userLogged']))
    elif request.method == 'POST' and request.form['user'] == 'test' and request.form['psw'] == 'test':
        session['userLogged'] = request.form['user']
        return redirect(url_for('profile', user=session['userLogged']))

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

# запустить сервер разработки : запустить скрипт python main.py

# тестовый контекст (без запуска if __name__ == '__main__':)
# with app.test_request_context():
#     print(url_for('profile', user='123', path='345'))
