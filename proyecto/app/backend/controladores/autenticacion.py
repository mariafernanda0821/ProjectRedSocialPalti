"""
login

registro

logout

"""
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from ..helper/process_err import process_error
from pymongo import MongoClient
## Establecemos conexión
client = MongoClient('mongodb://mongodb:27017/')
## Seleccionamos nuestra base de datos
db = client.palti


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
        return "<h1>missing_fields</h1>"
    return load_user(form)


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
