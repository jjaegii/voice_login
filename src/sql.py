import sqlite3
import os

connect = None
cursor = None

def connect():
    global connect, cursor
    connect = sqlite3.connect('database/sound.db')
    cursor = connect.cursor()
    cursor.execute("create table if not exists user(id text, password_path text)")

def insert(id, password_path):
    connect()
    sql = "insert into user values (?, ?)"
    cursor.execute(sql, (id, password_path))
    connect.commit()

def select(id):
    connect()
    sql = "select * from user where id = ?"
    cursor.execute(sql, (id))
    print(cursor.fetchone())
