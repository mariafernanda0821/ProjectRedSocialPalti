


"""

buscar usuario

editprofile



"""
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from ..helper.process_err import process_error
import os.path
from os import listdir
import json
from time import time
import datetime
import sys

def usr_editprofile():
    if "useremail" not in session:
        return process_error("Debes estar registrado e iniciar sesion para usar la app", url_for("login"), "Iniciar Sesion")
    if request.method == "GET":
        return render_template('editar/editarUsuario.html', title="Palti - My Profile", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"], session=session)
    elif request.method == "POST":
        form = request.form
        button = form.get('submit', None)
        if button == "cancel":
            return redirect(url_for("home"))
        elif button == "save":
            session["user-firstname"] = form["user-firstname"]
            session["user-lastname"] =  form["user-lastname"]
            session["useremail"] = form["useremail"]
            session["userpasswd"] = form["userpasswd"]
            session["userci"] = form["userci"]
            """session["favoritemusicuser"] = form["favoritemusicuser"]
            session["favoritegameuser"] = form["favoritegameuser"]
            session["favoritelanguajeuser"] = form["favoritelanguajeuser"]"""
            session["userbithdate"] = form["userbithdate"]
            session["usersex"] = form["usersex"]
            session["userabout"] = form["userabout"]
            update_user_from_session()
            return render_template('editar/editarUsuario.html', title="Palti - My Profile", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"], session=session)

def update_user_from_session():
    directory  = os.path.join(SITE_ROOT, "data")
    if not os.path.exists(directory):
        os.path.makedirs(directory)
    file_path = os.path.join(SITE_ROOT, "data/", session.get("useremail", "") )
    if os.path.isfile(file_path):
        data_user = {
           "user-firstname" : session["user-firstname"],
           "user-lastname" : session["user-lastname"],
           "useremail" : session["useremail"],
           "userpasswd" : session["userpasswd"],
           "userci" : session["userci"],
           "favoritemusicuser" : session["favoritemusicuser"],
           "favoritegameuser" : session["favoritegameuser"],
           "favoritelanguajeuser" : session["favoritelanguajeuser"],
           "userbithdate" : session["userbithdate"],
           "usersex" : session["usersex"],
           "userabout" : session["userabout"],
           "privacidad": session["privacidad"]
        }
        with open(file_path, "w") as f:
            json.dump(data_user, f)
