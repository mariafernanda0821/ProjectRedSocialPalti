# flask microframewok
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
#  image file uploaded
#from flask_uploads import UploadSet, IMAGES, configure_uploads

from backend.controladores.autenticacion import *
from backend.controladores.publicacion import *
from backend.controladores.usuario import *
from backend.controladores.chat import *
from backend.controladores.amigos import *

import os.path
from os import listdir
import json
from time import time
import datetime
import sys

## Importamos el cliente mongo
#from pymongo import MongoClient
## Establecemos conexión
#client = MongoClient('mongodb://mongodb:27017/')
## Seleccionamos nuestra base de datos
#db = client.palti
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
    return usr_editprofile()

@app.route("/friends")
def friends():
    return amg_friends()

#functions for login, singup, etc...
@app.route("/process_login", methods=["POST"])
def process_login():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(days=5)
    return aut_process_login()

@app.route("/process_register", methods=["POST"])
def process_register():
    return aut_process_register()

@app.route("/logout", methods=["GET"])
def logout():
    return aut_logout()

@app.route("/chat_messenger", methods=["GET"])
def chat_messenger():
    return chat_chat_messenger()

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

if __name__ == "__main__":
    app.run(port=8888, debug=True)
