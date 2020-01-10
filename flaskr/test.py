# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import sqlite3

conn = sqlite3.connect('sqlite_db')
cur = conn.cursor()
cur.execute('SELECT TOP 100 * FROM entries;')
print(cur.fetchall())
