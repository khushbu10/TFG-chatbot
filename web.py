from flask import Flask, render_template, request, make_response, url_for, json
from flask_mysqldb import MySQL
from requests.auth import HTTPBasicAuth
import API_service, requests
from functools import wraps
import datetime, config

app = Flask(__name__)
API_service = API_service.APIservice()

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth= request.authorization
        if auth and auth.username =='admin' and auth.password == 'admin':
            return f(*args, **kwargs)
        return make_response('Could not verify your login', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return (decorated)

@auth_required
def getCredentials():
    username = request.authorization.username
    passwd = request.authorization.password
    return (username, passwd)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notFound.html', error= 404)

#Mostrar todas las conversaciones
@app.route('/showConversations')
@auth_required
def viewConversations():
    conversations = API_service.getAllConversations(getCredentials()[0], getCredentials()[1])
    return render_template('index.html', conversations = conversations.json())    

#Mostrar la conversacion indicada (id)
@app.route('/getConversation/<id>')
@auth_required
def showConversation(id):
    conversations = API_service.getAllConversations(getCredentials()[0], getCredentials()[1])
    conversationbyUser = API_service.getConversationbyId(id, getCredentials()[0], getCredentials()[1])
    return render_template('index.html', conversations = conversations.json(), conversation = conversationbyUser.json(), id_conver=id)  
    
#Añadir mensaje a la conversación
@app.route('/addMessage/<id>', methods=['POST'])
@auth_required
def add_message(id):
    message = request.form['message']
    if message:
        API_service.addMessage(id, message, getCredentials()[0], getCredentials()[1])
    return showConversation(id)

#Añadir un usuario
@app.route('/addUser', methods=['POST'])
@auth_required
def addUser():
    name = request.form['name']
    surname = request.form['surname']
    access_point = request.form['access_point']
    if name and surname:
        API_service.addUser(name, surname, access_point, getCredentials()[0], getCredentials()[1])
    return viewConversations()


#Mostrar el formulario de usuario
@app.route('/userForm')
def show_addUserForm():
    return render_template('addUser.html')

#Mostrar todos los usuarios
@app.route('/showUsers')
@auth_required
def view_users():
    return render_template('users.html', users = API_service.getAllUsers(getCredentials()[0], getCredentials()[1]).json())  

#Descargar conversaciones 
@app.route('/downloadConversations')
@auth_required
def downloadConversation():
    conversations = API_service.getAllConversations(getCredentials()[0], getCredentials()[1])
    with open('test.txt', mode = 'wb') as file:
        file.write(conversations.content)
    return 'Se han descargado los datos correctamente'


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y%m%d')
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMMDD")

@app.route('/viewConversationbyDate/1', methods=['POST'])
@auth_required
def viewConversationbyDate():
    dateFrom = request.form['dateFrom']
    dateTo = request.form['dateTo']
    if validate(dateFrom) and validate(dateTo):
        try:
            conversationByDate= API_service.getConversationbyDate(dateFrom, dateTo, getCredentials()[0], getCredentials()[1])
            return render_template('conversationByDate.html', conversationByDate = conversationByDate.json()[0], dateFrom = dateFrom, dateTo = dateTo)
        except:
            return viewConversations()


#Inicializar y ejecutar
if __name__ == '__main__':
    app.run(port = config.webPort, debug = True)