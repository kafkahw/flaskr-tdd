# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)

# connect to database
def connect_db():
    """Connects to the database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    # Tell the datatbase to use the sqlite3.Row object ot represent rows.
    # This allows us to treat the rows as if they were dicts instead of tuples
    rv.row_factory = sqlite3.Row
    return rv

# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            contents = f.read()
            db.cursor().executescript(contents)
        db.commit()

# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    init_db()
    app.run()
