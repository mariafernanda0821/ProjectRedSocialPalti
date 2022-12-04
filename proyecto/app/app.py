# flask microframewok
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
#  image file uploaded
#from flask_uploads import UploadSet, IMAGES, configure_uploads

from backend.controladores.autenticacion import *
from backend.controladores.publicacion import *


import os.path
from os import listdir
import json
from time import time
import datetime
import sys

## Importamos el cliente mongo
from pymongo import MongoClient
## Establecemos conexión
client = MongoClient('mongodb://mongodb:27017/')
## Seleccionamos nuestra base de datos
db = client.palti
## Seleccionamos una colección
#my_coleccion= db.Nombre_Coleccion
## Operación que realizaremos sobre la colección
#my_coleccion.Funcion()


app = Flask(__name__)
app.secret_key = os.urandom(24)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
#app.config["UPLOADED_PHOTOS_DEST"] = "uploads"

#photos = UploadSet('userprofile', IMAGES)
#configure_uploads(app, photos)

@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    return aut_login()

@app.route("/register")
def register():
    return aut_register()

@app.route("/home")
def home():
    return aut_home()

@app.route("/editprofile", methods=["GET", "POST"])
def editprofile():
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


@app.route("/friends")
def friends():
    if "useremail" not in session:
        return process_error("Debes estar registrado e iniciar sesion para usar la app", url_for("login"), "Iniciar Sesion")
    return render_template('friends.html', title="Palti - Friends", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"])

#functions for login, singup, etc...
@app.route("/process_login", methods=["POST"])
def process_login():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(days=5)
    return aut_process_login()

@app.route("/process_register", methods=["POST"])
def process_register():
    fields = ['userprofile', 'user-firstname', 'user-lastname', 'useremail', 'userpasswd', 'userci', 'favoritemusicuser', 'favoritegameuser', 'favoritelanguajeuser', 'userbithdate', 'usersex']
    required_fields = ["user-firstname", "user-lastname", "useremail", "userpasswd", "userci"]
    missing_fields = []
    form = request.form
    for field in fields:
        field_value = form.get(field, None)
        if field in required_fields and (field_value == None or field_value == ""):
            missing_fields.append( field )
    if missing_fields:
        return "<h1>missing_fields</h1>";
    return register_user_in_db(form);

@app.route("/logout", methods=["GET"])
def logout():
    return aut_logout()

@app.route("/chat_messenger", methods=["GET"])
def chat_messenger():
    return render_template("chat_messenger.html", title="Palti - Chat Messenger", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"])

    '''
@app.route("/post_on_wall", methods=["POST"])
def post_on_wall():
    # using  Api fetch.
    #method render template post with message content and send to front
    user = session.get("user-firstname", None);
    message = request.form.get("message", None)
    question =  "Question example"
    #save in db
    timestamp = time()
    publicacion = {
      "_id" : f'{timestamp}{session["useremail"]}',
      "usuario" : session["useremail"],
      "fecha_creado" : timestamp,
      "contenido" : {
         "texto" : message,
         "multimedia" : ""
      },
      "tipo_privacidad" : "publico"
    }
    #save in user document...
    publicacion_db = db.publicacion
    publicacion_db.insert_one(publicacion).inserted_id
    return render_template("wallMsg.html", user=user, message=message, question=question )
    '''
#-------------------methods-------------------


def register_user_in_db(form):
    directory  = os.path.join(SITE_ROOT, "data")
    if not os.path.exists(directory):
        os.path.makedirs(directory)
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

def process_error(message, next_page, texto_boton):
    return render_template("error.html", error_message=message, next=next_page, texto_boton=texto_boton)

if __name__ == "__main__":
    app.run(port=8888, debug=True)
