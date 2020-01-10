# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

DATABASE = 'sqlite_db'


def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()

if __name__ == '__main__':
    app.run()
