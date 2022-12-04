"""
post en el muro

buscar publicaciones

home


"""
from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from ..helper.process_err import process_error


def aut_home():
    if "useremail" not in session:
        return process_error("Debes estar registrado e iniciar sesion para usar la app", url_for("login"), "Iniciar Sesion")
    return render_template('home.html',  title = "Palti - My Home", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"])
