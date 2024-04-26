from db_quer import *

class User:
    def __init__(self, id, email, password):
        self.__id = id
        self.__email = email
        self.__password = password

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def email(self):
        return self.__name

    @email.setter
    def email(self, mail):
        self.__email = mail

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

res = {}