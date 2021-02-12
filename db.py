#libreria json no el de flask
#libreria de mysql propia
from flask import jsonify, json
from flask_mysqldb import MySQLdb
import sys
from datetime import datetime
import config 

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class db(metaclass=SingletonMeta):
    def __init__ (self):
        pass
    def connect(self):
        try:
            mydb = MySQLdb.connect(
                config.mysqlhost,
                config.mysqluser,
                config.mysqlpasswd,
                config.mysqldb
            )
        except MySQLdb.Error as e:
            #escribir error en el fichero de LOG
            print('error {}: {}'.format(e.args[0], e.args[1]) )
            sys.exit(1)
        return mydb

    def getConversations(self):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('SELECT conversation.id_conver, message, id_agent, time_stamp, name FROM message INNER JOIN conversation ON conversation.id_conver = message.id_conver INNER JOIN users ON conversation.id_user = users.id_user WHERE conversation.id_conver=message.id_conver GROUP BY id_conver')
        data = cur.fetchall()
        cur.close()
        return jsonify(data)

    def getConversationUser(self, id):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('SELECT  message, id_agent, time_stamp, name, message.id_conver FROM message INNER JOIN conversation ON conversation.id_conver = message.id_conver INNER JOIN users ON conversation.id_user = users.id_user WHERE conversation.id_conver=%s',(id,))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)

    def getMessages(self):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('SELECT * FROM message ORDER BY time_stamp')
        data = cur.fetchall()
        cur.close()
        return jsonify(data)

    def addMessageConversation(self, id, message):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('INSERT INTO message (time_stamp, message, id_conver, id_agent) VALUES (%s, %s, %s, %s)', 
                (datetime.now(), message, id, 1))
        conn.commit()
        cur.close()
        return jsonify('Mensaje insertado')

    def getUsers(self):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute ('SELECT conversation.id_user, name, surname, access_point, COUNT(*) AS conversations FROM conversation INNER JOIN users WHERE users.id_user= conversation.id_user GROUP BY users.id_user')
        data = cur.fetchall()
        cur.close()
        return jsonify(data)

    def addUsers(self, name, surname, access):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, surname, access_point) VALUES (%s, %s, %s)', (name, surname, access))
        conn.commit()
        cur.close()
        return jsonify('Usuario ha sido insertado')

    def get_user(self, id):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        return jsonify(data[0])

    def update_user(self, id, name, surname, access):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('UPDATE users SET name = %s, surname= %s, access_point= %s WHERE id= %s', (name, surname, access, id))
        conn.commit()
        cur.close()
        return jsonify('Usuario ha sido actualizado correctamente')

    def delete_user(self, id):
        conn = db.connect(self)
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        return jsonify('User Removed Successfully')

    def getConversationsbyDate(self, dateFrom, dateTo):
        conn = db.connect(self)
        cur = conn.cursor()
        cur. execute('SELECT COUNT(DISTINCT id_conver) FROM message WHERE time_stamp BETWEEN %s and %s', (dateFrom, dateTo))
        data = cur.fetchall()
        print(data)
        cur.close()
        return jsonify(data)