from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,json, make_response
from flask_mysqldb import MySQL
from functools import wraps
from datetime import datetime

import db
import config
app = Flask(__name__)
mydb = db.db()
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth= request.authorization
        if auth and auth.username =='admin' and auth.password == 'admin':
            return f(*args, **kwargs)
        return make_response('Could not verify your login', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notFound.html', error= 404)

#Mostrar todas las conversaciones
@app.route('/showConversations', methods=['GET'])
@auth_required
def show_conversations():
    return mydb.getConversations()
  
#Mostrar todas las conversaciones del usuario indicado
@app.route('/showConversation/<id>', methods=['GET'])
@auth_required
def show_conversation(id):
    return mydb.getConversationUser(id)

#Mostrar todos los mensajes
@app.route('/viewMessages')
@auth_required
def view_messages():
    return mydb.getMessages()

#Añadir un mensaje a una conversacion
@app.route('/addMessage/<id>', methods=['POST'])
@auth_required
def addMessage(id):
    message = request.args.get('message')
    if(message is None):
        return 'Error: No message field provided'
    else:
        return mydb.addMessageConversation(id, message)

#Mostrar todos los usuarios
@app.route('/viewUsers')
@auth_required
def viewUser():
    return mydb.getUsers()

#Añadir un usuario
@app.route ('/addUser', methods=['POST'])
@auth_required
def addUser(): 
    if 'name' in request.args and 'surname' in request.args:
        name = request.args.get('name')
        surname = request.args.get('surname')
        if (request.args.get('access_point') == '1'):
            access = 'Navegador Web'
        elif (request.args.get('access_point') == '2'):
            access = "Telegram"
        else:
            access = "Unknown Source"
        return mydb.addUsers(name, surname, access)
    else:
        return 'Error: No name or surname field provided'

#Editar un usuario
@app.route ('/getUser/<id>')
@auth_required
def getUser(id):
    return mydb.getUser(id)
    
@app.route ('/updateUser/<id>', methods=['PUT'])
@auth_required
def updateUser(id):
    #cOMPROBAR PARAMETROS
    name = request.form['name']
    surname = request.form['surname']
    access = request.form['access_point']
    if(name is None or surname is None or access is None):
        return 'Falta rellenar campos'
    return mydb.updateUser(name, surname, access, id)
        
#Eliminar un usuario
@app.route ('/deleteUser/<string:id>', methods=['DELETE'])
@auth_required
def deleteUser(id):
    return mydb.deleteUser(id)

@app.route('/getConversationbyDate')
@auth_required
def getConversationbyDate():

    dateFrom = request.args.get('dateFrom')
    dateTo = request.args.get('dateTo')
    if dateFrom and dateTo:
        return mydb.getConversationsbyDate(dateFrom, dateTo)
    return 'Error - No se han recibido las fechas'

#Inicializar y ejecutar
if __name__ == '__main__':
    app.run(port = config.apiPort, debug = True)