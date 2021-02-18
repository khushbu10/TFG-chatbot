from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth


#Este archivo es un enlace entre web.py y API
import config
class APIservice():
    def __init__ (self):
        pass
    
    def getAllConversations(self, username, password):
        url = urljoin (config.host, "/show_conversations")
        return requests.get(url, auth=HTTPBasicAuth(username, password))

    def getConversationbyId(self, id, username, password):
        url = urljoin (config.host, "show_conversation/%s" %(id))
        return requests.get(url,auth=HTTPBasicAuth(username, password))

    def addMessage(self, id, message, username, password):
        url = urljoin (config.host, "addMessage/%s" %(id))
        return requests.post(url, auth=HTTPBasicAuth(username, password), params={'message': message})

    def addUser(self, name, surname, access_point, username, password):
        url = urljoin (config.host, "addUser")
        return requests.post(url, params={'name': name, 'surname': surname, 'access_point':access_point}, auth=HTTPBasicAuth(username, password))

    def getAllUsers(self, username, password):
        url = urljoin (config.host, "/view_users")
        return requests.get(url, auth=HTTPBasicAuth(username, password))
    
    def getConversationbyDate(self, dateFrom, dateTo, username, password):
        url = urljoin(config.host, "/getConversationbyDate")
        return requests.get(url, params={'dateFrom': dateFrom, 'dateTo': dateTo}, auth=HTTPBasicAuth(username, password))