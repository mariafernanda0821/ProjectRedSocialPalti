"""
login

registro

logout

"""
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from ..helper.process_err import process_error
import os.path
import os
from os import listdir
import json
from time import time
import datetime
import sys

from pymongo import MongoClient
## Establecemos conexión
client = MongoClient('mongodb://mongodb:27017/')
## Seleccionamos nuestra base de datos
db = client.palti

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

def aut_login():
     """
     when user acess into webpage domain,
     server shows them login or home if user is in session
     :return: content of register.html or login.html
     """
     if 'useremail' in session:
         return redirect( url_for('home') )
     return render_template('login.html', title="Palti - Login", form_title="Iniciar Sesion", login_or_register_href="register", login_or_register_text="Registrar")


def aut_register():
    if 'useremail' in session:
        return redirect( url_for('home') )
    return render_template('register.html', title="Palti - Register", form_title="Registartse", login_or_register_href="login" ,login_or_register_text="Iniciar Sesion")


def aut_logout():
    if "useremail" in session:
        #save_current_user()
        session.pop("useremail", None)
        session.clear()
        return redirect(url_for("login"))
    return process_error("No hay sesion de usuario abierta", url_for("login"), "Iniciar Sesion")


def aut_process_login():
    missing_fields = []
    fields = ["useremail", "userpasswd"]
    form = request.form
    for field in fields:
        field_value = form.get(field, None)
        if field == None or field == "":
            missing_fields.append( field )
    if missing_fields:
        return process_error("Especifique todos los campos para iniciar sesion", url_for("login"), "Volver a Inicio de Sesion")
    return load_user(form)

def aut_process_register():
    fields = ['userprofile', 'user-firstname', 'user-lastname', 'useremail', 'userpasswd', 'userci', 'favoritemusicuser', 'favoritegameuser', 'favoritelanguajeuser', 'userbithdate', 'usersex']
    required_fields = ["user-firstname", "user-lastname", "useremail", "userpasswd", "userci"]
    missing_fields = []
    form = request.form
    for field in fields:
        field_value = form.get(field, None)
        if field in required_fields and (field_value == None or field_value == ""):
            missing_fields.append( field )
    if missing_fields:
        return process_error("Para registrarse, debe indicar por lo menos los campos Nombre, Apellido, correo, contraseña y cedula", url_for("register"), "Volver a Registro de Usuario" )
    return register_user_in_db(form);

def register_user_in_db(form):
    directory  = os.path.join(SITE_ROOT, "data")
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(SITE_ROOT, "data/", form["useremail"])
    if os.path.isfile(file_path):
        return process_error("El usuario ya existe", url_for("register"), "Volver a Registro de Usuario")

    data_user = {
        "userprofile" : form["userprofile"],
        "user-firstname" : form["user-firstname"],
        "user-lastname" : form["user-lastname"],
        "useremail" : form["useremail"],
        "userpasswd" : form["userpasswd"],
        "userci" : form["userci"],
        "favoritemusicuser" : form["favoritemusicuser"].split(','),
        "favoritegameuser" : form["favoritegameuser"].split(','),
        "favoritelanguajeuser" : form["favoritelanguajeuser"].split(','),
        "userbithdate" : form["userbithdate"],
        "usersex" : form["usersex"],
        "userabout" : form["userabout"],
        "privacidad" : {
            "comentarios": True,
            "sub_comentarios": True,
            "publicaciones": True,
            "datos_personales": {
                "password": False,
                "ci": False,
                "nombre": True,
                "apellido": True,
                "email": True,
                "fecha_nacimiento": True,
                "descripcion_personal": True,
                "color_favorito": True,
                "musica_favorito": True,
                "video_juego_favorito": True,
                "lenguaje_favorito": True
            }
        }
    }
    #with open(file_path, "w") as f:
    #    json.dump(data_user, f)
    user = db.user
    user.insert_one(data_user).inserted_id

    #post_id
    session["userprofile"] = form["userprofile"],
    session["user-firstname"] = form["user-firstname"],
    session["user-lastname"] = form["user-lastname"],
    session["useremail"] = form["useremail"],
    session["userpasswd"] = form["userpasswd"],
    session["userci"] = form["userci"],
    session["favoritemusicuser"] = form["favoritemusicuser"],
    session["favoritegameuser"] = form["favoritegameuser"],
    session["favoritelanguajeuser"] = form["favoritelanguajeuser"]
    session["userbithdate"] = form["userbithdate"]
    session["usersex"] = data_user["usersex"]
    return redirect(url_for("home"))

def load_user(form):
    '''
    It loads data for the given user (identified by email) from the data directory.
    It looks for a file whose name matches the user email
    :return: content of the home page (app basic page) if user exists and password is correct
    '''
    #file_path = os.path.join(SITE_ROOT, "data/", form["useremail"])
    newUser = db.get_collection('user')
    searchUser = newUser.find_one({'useremail': form["useremail"]})
    #print("searchUser", searchUser)
    if not searchUser :
        return process_error("Usuario no encontrado", url_for("login"), "Volver a Inicio de Sesion")

    if searchUser["userpasswd"] != form["userpasswd"] :
        return process_error("Contraseña incorrecta", url_for("login"), "Volver a Inicio de Sesion")

    """ if not os.path.isfile(file_path) :
        return process_error("Usuario no encontrado", url_for("login"), "Volver a Inicio de Sesion")
    with open(file_path, "r") as f:
        data_user = json.load(f)
    if data_user["userpasswd"] != form["userpasswd"]:
        return process_error("Contraseña incorrecta", url_for("login"), "Volver a Inicio de Sesion") """

    #session.permanent = True
    #app.permanent_session_lifetime = datetime.timedelta(days=5)
    session["id"] = str(searchUser['_id'])
    session["user-firstname"] = searchUser["user-firstname"]
    session["user-lastname"] =  searchUser["user-lastname"]
    session["useremail"] = searchUser["useremail"]
    session["userpasswd"] = searchUser["userpasswd"]
    session["userci"] = searchUser["userci"]
    session["favoritemusicuser"] = searchUser["favoritemusicuser"]
    session["favoritegameuser"] = searchUser["favoritegameuser"]
    session["favoritelanguajeuser"] = searchUser["favoritelanguajeuser"]
    session["userbithdate"] = searchUser["userbithdate"]
    session["usersex"] = searchUser["usersex"]
    session["userabout"] = searchUser["userabout"]
    session["privacidad"] = searchUser["privacidad"]
    print(session)
    # app.permanent_session_lifetime = datetime.timedelta(days=5)
    # session["user-firstname"] = data_user["user-firstname"]
    # session["user-lastname"] =  data_user["user-lastname"]
    # session["useremail"] = data_user["useremail"]
    # session["userpasswd"] = data_user["userpasswd"]
    # session["userci"] = data_user["userci"]
    # session["favoritemusicuser"] = data_user["favoritemusicuser"]
    # session["favoritegameuser"] = data_user["favoritegameuser"]
    # session["favoritelanguajeuser"] = data_user["favoritelanguajeuser"]
    # session["userbithdate"] = data_user["userbithdate"]
    # session["usersex"] = data_user["usersex"]
    # session["userabout"] = data_user["userabout"]
    #session['privacidad'] = data_user['privacidad']
    return redirect(url_for("home"))
