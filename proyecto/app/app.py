# flask microframewok
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
#  image file uploaded
#from flask_uploads import UploadSet, IMAGES, configure_uploads
 

import os.path
from os import listdir
import json
from time import time
import datetime
import sys

## Importamos el cliente mongo
from pymongo import MongoClient
## Establecemos conexión
client = MongoClient('mongodb://172.17.0.2:27017/')
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
    """
    when user acess into webpage domain,
    server shows them login or home if user is in session
    :return: content of register.html or login.html
    """
    if 'useremail' in session:
        return redirect( url_for('home') )
    return render_template('login.html', title="Palti - Login", form_title="Iniciar Sesion", login_or_register_href="register", login_or_register_text="Registrar")

@app.route("/register")
def register():
    if 'useremail' in session:
        return redirect( url_for('home') )
    return render_template('register.html', title="Palti - Register", form_title="Registartse", login_or_register_href="login" ,login_or_register_text="Iniciar Sesion")

@app.route("/home")
def home():
    if "useremail" not in session:
        return process_error("Debes estar registrado e iniciar sesion para usar la app", url_for("login"), "Iniciar Sesion")
    return render_template('home.html',  title = "Palti - My Home", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"])

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
    missing_fields = []
    fields = ["useremail", "userpasswd"]
    form = request.form
    for field in fields:
        field_value = form.get(field, None)
        if field == None or field == "":
            missing_fields.append( field )
    if missing_fields:
        return "<h1>missing_fields</h1>"
    return load_user(form)

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
    if "useremail" in session:
        #save_current_user()
        session.pop("useremail", None)
        session.clear()
        return redirect(url_for("login"))
    return process_error("No hay sesion de usuario abierta", url_for("login"), "Iniciar Sesion")

@app.route("/chat_messenger", methods=["GET"])
def chat_messenger():
    return render_template("chat_messenger.html", title="Palti - Chat Messenger", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"])


@app.route("/post_on_wall", methods=["POST"])
def post_on_wall():
    print(request)

    user = session.get("user-firstname", None);
    message = request.form.get("message", None)
    question =  "Question example"

    return render_template("wallMsg.html", user=user, message=message, question=question )

#-------------------methods-------------------
def load_user(form):
    file_path = os.path.join(SITE_ROOT, "data/", form["useremail"])
    newUser = db.get_collection('user')
    searchUser = newUser.find_one({'useremail': form["useremail"]})
    print("searchUser", searchUser)
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

    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(days=5)
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
    with open(file_path, "w") as f:
        json.dump(data_user, f)
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
