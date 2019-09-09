import MySQLdb
import MySQLdb.cursors
import os
import sqlite3
from core import Config

connection = None
mode = 'mysql'

def getRows(sql, params = None):
    global connection
    global mode

    # sqlite compat
    if mode == 'sqlite' and sql == 'SELECT LAST_INSERT_ID() AS insert_id':
        sql = 'SELECT last_insert_rowid() AS insert_id'

    if mode == 'sqlite':
        sql = sql.replace('%s', '?')

    cur = connection.cursor()

    if not params:
        cur.execute(sql)
    else:
        cur.execute(sql, params)

    data = cur.fetchall()

    return data

def execute(sql, params = None):
    global connection
    global mode

    if mode == 'sqlite':
        sql = sql.replace('%s', '?')

    cur = connection.cursor()

    if not params:
        cur.execute(sql)
    else:
        cur.execute(sql, params)

def connect():    
    """ Connects to the database """
    global connection
    global mode
    
    if Config.getValue('SQLITE') == 'yes':
        mode = 'sqlite'

    if mode == 'mysql':
        db =  MySQLdb.connect(host=Config.getValue('DB_HOST'), user=Config.getValue('DB_USER'), password=Config.getValue('DB_PASS'), database=Config.getValue('DB_NAME'), cursorclass=MySQLdb.cursors.DictCursor, use_unicode=True, charset="utf8mb4")
        db.autocommit(True)
    else:
        db = sqlite3.connect('system.db')
        db.row_factory = sqlite3.Row
        db.isolation_level = None

    connection = db
    #return db

def disconnect():
    global connection

    connection.close()

def createSQLite():
    create_sql = open(os.path.join(os.path.dirname(__file__), '../schema/sqlite.sql'), 'r').read()
    sqlite3.complete_statement(create_sql)

    conn = sqlite3.connect('system.db')
    cursor = conn.cursor()

    try:
        cursor.executescript(create_sql)
    except Exception as e:
        print(e)

    conn.close()