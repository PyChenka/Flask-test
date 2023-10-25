import psycopg2
from flask import g

from config import app


# подключение к БД
def connect_to_db():
    conn = psycopg2.connect(
        database=app.config['DATABASE']['NAME'],
        user=app.config['DATABASE']['USER'],
        password=app.config['DATABASE']['PASSWORD'],
        host=app.config['DATABASE']['HOST'],
        port=app.config['DATABASE']['PORT'],
        options=app.config['DATABASE']['OPTIONS'],
    )
    return conn


# создание таблиц в БД
def create_db_tables():
    conn = connect_to_db()

    # из файла
    with app.open_resource('db_tables.sql', mode='r') as f:
        conn.cursor().execute(f.read())
        conn.commit()
        conn.close()

    # cur = conn.cursor()
    #
    # cur.execute('DROP TABLE IF EXISTS books;')
    # cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
    #             'title varchar (150) NOT NULL,'
    #             'author varchar (50) NOT NULL,'
    #             'pages_num integer NOT NULL,'
    #             'review text,'
    #             'date_added date DEFAULT CURRENT_TIMESTAMP);'
    #             )
    #
    # cur.execute('INSERT INTO books (title, author, pages_num, review)'
    #             'VALUES (%s, %s, %s, %s)',
    #             ('A Tale of Two Cities',
    #              'Charles Dickens',
    #              489,
    #              'A great classic!')
    #             )
    #
    # cur.execute('INSERT INTO books (title, author, pages_num, review)'
    #             'VALUES (%s, %s, %s, %s)',
    #             ('Anna Karenina',
    #              'Leo Tolstoy',
    #              864,
    #              'Another great classic!')
    #             )
    #
    # conn.commit()
    #
    # cur.close()
    # conn.close()


# создать соединение c БД
def open_db_connection():
    if not hasattr(g, '_database'):
        g._database = connect_to_db()
    return g._database


# закрыть соединение с БД
@app.teardown_appcontext    # срабатывает в момент уничтожения контекста приложения
def close_db_connection(exception):
    if hasattr(g, '_database'):
        g._database.close()